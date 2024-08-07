import { createRequire } from "module";
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const require = createRequire(import.meta.url);
const express = require("express");
const axios = require('axios');
const fs = require('fs');

const path = require('path');
const fileUpload = require("express-fileupload");
const cors = require("cors");
const { exec } = require("child_process");
const { execFile } = require("child_process");
const app = express();
app.use(express.json());
const downloadPath = join(__dirname, 'downloads');
app.use(
  cors({
    origin: "http://localhost:*",
    optionsSuccessStatus: 200,
  })
);
app.use(fileUpload());

// Function to execute Python script
function executePythonScript(tcrAlpha,tcrBeta,res) {
  execFile(
    "python",
    ["server/models/search_pdb.py", tcrAlpha,tcrBeta,],
    { encoding: "utf8" },
    (error, stdout, stderr) => {
      console.log("Received stdout:", stdout);
      if (error) {
        console.error(`exec error: ${error}`);
        return res.status(500).send(`Error processing your query: ${stderr}`);
      }
      // const results = JSON.parse(stdout);
      // res.json(results);
      try {
        const results = JSON.parse(stdout);
        if (results.length === 0) {
          console.log("No matches found.");
          res.status(404).send("No matches found.");
        } else {
          res.json(results);
        }
      } catch (parseError) {
        console.error("Error parsing output:", parseError);
        res.status(500).send("Error parsing output");
      }
    }
  );
}


app.post("/api/submitSequences", async (req, res) => {
  const { tcrAlpha, tcrBeta } = req.body;
  // if (!tcrAlpha || !tcrBeta) {
  //   return res.status(400).send("Incomplete TCR sequences provided.");
  // }
  
  console.log(
    "Sending TCR alpha and beta sequences to Python script:",
    tcrAlpha,
    tcrBeta
  );
  // Call the function to execute the Python script with the combined sequences
  executePythonScript(tcrAlpha, tcrBeta, res);
});



app.post("/api/submitFile", (req, res) => {
  if (!req.files || !req.files.file) {
    return res.status(400).send("No files were uploaded.");
  }

  const file = req.files.file;
  const sequenceData = file.data.toString(); // Get file content as a string
  console.log("Received file content for parsing:", sequenceData);

  // Parse the FASTA data to extract sequences
  const sequences = parse_fasta(sequenceData);
  if (sequences.length === 0) {
    return res.status(400).send("No valid sequences found in the file.");
  }

  const tcr_alpha = sequences[0];
  const tcr_beta = sequences[1];

  // Call the function to execute the Python script with the formatted sequences
  executePythonScript(tcr_alpha, tcr_beta, res);
});

// Function to parse FASTA formatted data
function parse_fasta(fasta_data) {
  let sequences = [];
  let current_sequence = "";
  fasta_data.split("\n").forEach((line) => {
    line = line.trim();
    if (line.startsWith(">")) {
      if (current_sequence) {
        sequences.push(current_sequence);
        current_sequence = ""; // Reset for next sequence
      }
    } else {
      current_sequence += line;
    }
  });
  if (current_sequence) {
    sequences.push(current_sequence); // Add the last sequence if any
  }
  return sequences;
}

app.get('/api/download-pdb/:pdbId', (req, res) => {
  const pdbId = req.params.pdbId;
  const filePath = path.join(__dirname, 'downloads', `${pdbId}.pdb`);

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.status(404).send('File not found');
      return;
    }
    res.type('text/plain');
    res.send(data);
  });
});

app.post('/api/downloadPDB', async (req, res) => {
  const pdbId = req.body.pdbId;  
  if (!pdbId) {
      return res.status(400).send('PDB ID is required');
  }

  try {
      await downloadPDBFile(pdbId);
      res.send({ message: 'Download started successfully' });
  } catch (error) {
      console.error('Failed to download file:', error);
      res.status(500).send('Failed to download file');
  }
});
async function downloadPDBFile(pdbId) {
  const url = `https://files.rcsb.org/download/${pdbId}.pdb`;
  const outputPath = join(downloadPath, `${pdbId}.pdb`);

  const response = await axios({
      method: 'get',
      url: url,
      responseType: 'stream'
  });

  const writer = fs.createWriteStream(outputPath);

  response.data.pipe(writer);

  return new Promise((resolve, reject) => {
      writer.on('finish', resolve);
      writer.on('error', reject);
  });
}


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

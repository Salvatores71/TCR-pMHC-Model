<template>
  <div class="content">
    <h1>Results</h1>
    <div class="layout">
      <div class="table-container">
        <!-- <p>The searched sequences:{{ results[0].sequence }}</p> -->
        <p v-if="results.length === 0">No results found.</p>
        <p v-else>Total results: {{ results.length }}</p>

        <el-table :data="results" style="width: 100%" v-if="results.length > 0">
          <el-table-column prop="model_id" label="PDB ID" width="180">
            <template #default="{ row }">
              <el-button type="" @click="viewDetails(row.model_id)">{{
                row.model_id
              }}</el-button>
            </template>
          </el-table-column>
          <!-- <el-table-column
        prop="sequence"
        label="Sequence"
        width="200"
      ></el-table-column> -->
          <el-table-column
            prop="score"
            label="Score"
            width="100"
          ></el-table-column>
          <el-table-column label="Display Structure" width="180">
            <template #default="{ row }">
              <el-button type="primary" @click="displayStructure(row.model_id)"
                >Display</el-button
              >
            </template>
          </el-table-column>
          <el-table-column prop="model_id" label="Explore" width="180">
            <template #default="{ row }">
              <el-button type="primary" @click="Explore(row.model_id)">Explore</el-button>
            </template>
          </el-table-column>

          <el-table-column label="Download" width="180" prop="model_id">
            <template #default="{ row }">
              <el-button type="primary" @click="downloadFile(row.model_id)"
                >Download</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div v-show="show3DViewer" id="3d-viewer" class="viewer_3Dmoljs"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useResultsStore } from "../stores/useResultsStore";
import { usePdbStore } from '../stores/pdbStore';
import axios from "axios";
import { ElMessage } from "element-plus";
import $ from "jquery"; 
import { useRouter } from "vue-router";
export default defineComponent({
  setup() {
    const pdbStore = usePdbStore();
    const store = useResultsStore();
    const router = useRouter();
    const show3DViewer = ref(false); // Controls visibility of the 3D viewer
    const results = store.results;
    onMounted(() => {
      if (store.results.length > 0) {
        // Auto download the first result
        // downloadFile(store.results[0].model_id);
        render3DStructure(store.results[0].model_id);
      }
    });
    const Explore=(pdbId)=>{
      pdbStore.setPdbId(pdbId);
      router.push({ name: '3DViewer' });
    }
    const viewDetails = (pdbId) => {
      
      router.push({ name: "PDBDetails", params: { id: pdbId } });
    };
    const render3DStructure = (pdbId) => {
      const element = document.getElementById("3d-viewer");
      if (element) {
        const config = { backgroundColor: "white" };
        const viewer = new $3Dmol.createViewer(element, config);
        const pdbUri = `/api/download-pdb/${pdbId}`;

        $.ajax({
          url: pdbUri,
          success: function (data) {
            viewer.addModel(data, "pdb");
            viewer.setStyle({}, { cartoon: { color: "spectrum" } });
            viewer.zoomTo();
            viewer.render();
            viewer.zoom(1.2, 1000); 
            show3DViewer.value = true; 
          },
          error: function (xhr, status, err) {
            console.error(`Failed to load PDB file from ${pdbUri}`, err);
            ElMessage.error("Failed to load the 3D structure.");
          },
        });
      } else {
        ElMessage.error("3D viewer element not found.");
      }
    };
    const displayStructure = (pdbId) => {
      const element = document.getElementById("3d-viewer");
      if (!element) {
        console.error("3D viewer element not found.");
        return;
      }

      const viewer = new $3Dmol.createViewer(element, {
        backgroundColor: "white",
      });

      // Assuming the PDB files are served from a static directory
      const pdbUri = `/api/download-pdb/${pdbId}`;

      // Fetch and display the PDB file
      fetch(pdbUri)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.text();
        })
        .then((data) => {
          ElMessage.success("Display structure successfully");
          viewer.addModel(data, "pdb");
          viewer.setStyle({}, { cartoon: { color: "spectrum" } });
          viewer.zoomTo();
          viewer.render();
        })
        .catch((error) => {
          console.error("Failed to load PDB file:", error);
        });
    };
    
    const downloadFile = (pdbId) => {
      const config = {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      };
      axios
        .post("/api/downloadPDB", { pdbId }, config)
        .then(() => {
          ElMessage.success("Download started!");
        })
        .catch((error) => {
          console.error("Error downloading the file:", error);
          alert("Failed to start download.");
        });
    };

    return {
      results,
      downloadFile,
      show3DViewer,
      displayStructure,
      viewDetails,
      Explore,
    };
  },
});
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 50px;
}

.layout {
  display: flex;
  width: 100%;
}

.table-container {
  flex: 1;
  text-align: center;
  padding: 20px;
  border-right: 1px solid #ccc; /* Optional: adds a border between the table and the viewer */
}

.viewer_3Dmoljs {
  position: relative;
  width: 50%; 
  height: 500px; 
  border: 1px solid #ccc;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  margin-bottom: 20px;
}

.upload-instruction {
  margin-top: 10px;
}
</style>

<template>
  <el-tabs
    v-model="activeName"
    type="card"
    class="demo-tabs"
    @tab-click="handleClick"
  >
    <el-tab-pane label="Paste Sequence" name="first">
      <div class="flex flex-col h-400">
        <el-form
          label-position="left"
          label-width="180px"
          class="tcr-form"
          ref="tcrForm"
        >
          <el-form-item label="Enter TCR α sequence">
            <el-input
              v-model="tcrAlpha"
              type="textarea"
              :rows="2"
              class="input-field"
            ></el-input>
          </el-form-item>
          <el-form-item label="Enter TCR β sequence">
            <el-input
              v-model="tcrBeta"
              type="textarea"
              :rows="2"
              class="input-field"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitSequences"
              >Submit</el-button
            >
            <el-button @click="resetForm">Reset</el-button>
            <el-button @click="useExample">Use Example</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-tab-pane>
    <el-tab-pane label="Upload File" name="second">
      <div class="flex flex-col h-400">
        <div class="font-600 text-3xl ml-1">
          1. Input Sequence
          <el-button type="primary" class="text-lg">
            <a
              href="https://tcrmodel.ibbr.umd.edu/static/example/example_fasta_ub.fasta"
              target="_blank"
              class="el-link--inner"
              >See Example FASTA sequence</a
            >
          </el-button>
        </div>
        <el-divider border-style="double" />
        <div
          class="rounded w-190 h-90 mt-10 rounded-2xl"
          style="box-shadow: 0 0 64px #cfd5db"
        >
          <el-upload
            class="upload-demo"
            drag
            :http-request="handleFileUpload"
            :on-remove="remove"
            :file-list="fileList"
            :multiple="false"
            accept=".fasta,.fa"
            ref="uploadRef"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="flex flex-col justify-center items-center">
              <div class="text-[90px] mt-10" style="color: #028090">
                <i class="el-icon-upload"></i>
              </div>
              <p class="text-h5 mt-3 font-light" style="color: #028090">
                Click or drag a file to this area to upload your file
              </p>
              <p
                class="text-sp mt-3 mb-3 text-opacity-100"
                style="color: #f07167"
              >
                Fasta file size should be less than 10MB
              </p>
              <p class="text-sp mb-3 text-opacity-100" style="color: #f07167">
                Supported formats: .fasta / .fa
              </p>
            </div>
          </el-upload>
        </div>
        <div
          class="mt-15 flex flex-row justify-center"
          style="width: 100%; text-align: center"
        >
          <el-button
            size="large"
            style="color: #34498e"
            class="text-white hover:text-white focus:text-white active:text-white text-2xl"
            @click="submit"
          >
            Submit
          </el-button>
        </div>

        <!-- Text Area for Displaying Uploaded File Content -->
        <el-input
          type="textarea"
          v-model="fileContent"
          :rows="10"
          placeholder="Uploaded file content will appear here..."
          class="mt-4"
        ></el-input>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ElMessage } from "element-plus";
import { ref, defineComponent } from "vue";
import { UploadFilled } from "@element-plus/icons-vue";
import type { TabsPaneContext, ElMessageBox } from "element-plus";
import axios from "axios";
import { useRouter } from "vue-router";
import { useResultsStore } from "../stores/useResults";
import { ElLoading } from "element-plus";
const store = useResultsStore();
const tcrAlpha = ref("");
const tcrBeta = ref("");
const tcrForm = ref(null);
const fileContent = ref("");
const fileList = ref([]);
const activeName = ref("first");
const router = useRouter();
const submitSequences = async () => {
  try {
    const payload = {
      tcrAlpha: tcrAlpha.value,
      tcrBeta: tcrBeta.value,
    };
    console.log(tcrAlpha)
    console.log(tcrBeta)

    // const payload = {
    //   tcrAlpha: tcrAlpha.value,
    //   ...(tcrBeta.value && { tcrBeta: tcrBeta.value }),
    // };
    console.log(payload)
    const config = {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    };
    ElMessage({
      showClose: true,
      message: "Sequences submitted!",
      type: "success",
    });
    ElMessage({
      showClose: true,
      message: "Please wait for the result",
      type: "success",
    });
    const loading = ElLoading.service({
      lock: true,
      text: "Loading",
      background: "rgba(0, 0, 0, 0.7)",
    });
    
    try {
      const response = await axios.post(
        "/api/submitSequences",
        payload,
        config
      );
      store.setResults(response.data.results);

      
      router.push({ name: "result" });
    } catch (error) {
      console.error("Error submitting sequences:", error);
      
    } finally {
      
      loading.close();
    }
  } catch (error) {
    console.error("Error submitting sequences:", error);
    ElMessage.error("Error submitting sequences");
  }
};

const resetForm = () => {
  tcrAlpha.value = "";
  tcrBeta.value = "";
  fileList.value = [];
};
const useExample = () => {
  tcrAlpha.value =
    "VTQIPAALSVPEGENLVLNCSFTDSAIYNLQWFRQDPGKGLTSLLLIQSSQREQTSGRLNASLDKSSGRSTLYIAASQPGDSATYLCAVMGTTDSWGKLQFGAGTQVVVTP";
  tcrBeta.value =
    "VTQTPKHLITATGQRVTLRCSPRSGDLSVYWYQQSLDQGLQFLIQYYNGEERAKGNILERFSAQQFPDLHSELNLSSLELGDSALYFCASSVATYSTDTQYFGPGTRLTVL";
};

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event);
};
const handleFileUpload = async (uploadEvent) => {
  const file = uploadEvent.file;
  const reader = new FileReader();
  reader.onload = (e) => {
    fileContent.value = e.target.result;
    console.log("File loaded:", fileContent.value); 
  };
  reader.onerror = (e) => {
    console.error("Error reading file:", e);
  };
  reader.readAsText(file);
};

const remove = (file) => {
  fileContent.value = "";
  ElMessage({
    type: "info",
    message: "File removed",
  });
};
const submit = async () => {
  const formData = new FormData();
  try {
    formData.append(
      "file",
      new Blob([fileContent.value], { type: "text/plain" })
    );
    console.log("Submitted file content:", fileContent.value);

    ElMessage({
      showClose: true,
      message: "File content submitted!",
      type: "success",
    });
    ElMessage({
      showClose: true,
      message: "Please wait for the result",
      type: "success",
    });
  } catch (error) {
    console.error("Error during submission:", error);
    ElMessage.error("An error occurred during submission");
  }

  try {
    const response = await axios.post("/api/submitFile", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*",
      },
    });
    console.log("Received PDB IDs:", response.data);
    store.setResults(response.data.results);
    router.push({ name: "result" });
  } catch (error) {
    console.error("Error submitting the file:", error);
    ElMessage.error("Error submitting the file");
  }
};
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.el-link--inner {
  color: inherit; 
  text-decoration: none; 
}
.tcr-form {
  max-width: 800px; 
  margin: 20px; 
}
.input-field {
  width: 100%; 
}
</style>

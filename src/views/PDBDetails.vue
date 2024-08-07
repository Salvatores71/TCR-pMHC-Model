<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="500px">
        <div>
          <el-carousel indicator-position="outside">
    <el-carousel-item v-for="(item, index) in imageItems" :key="index">
      <div class="carousel-item-content">
        <img :src="item.url" alt="Protein Structure" class="img-fluid" />
        <div class="label">{{ item.label }}</div>
      </div>
    </el-carousel-item>
  </el-carousel>
        </div>
      </el-aside>
      <el-main>
        <div class="col-md-8">
          
          <div v-if="entry">
            <p>
              {{ entry.rcsb_id }}
            </p>
            <p>Struct Title:{{ entry.struct.title }}</p>
            <p>
              PDB DOI:
              <a :href="'https://doi.org/10.2210/pdb' + entry.rcsb_id + '/pdb'">
                https://doi.org/10.2210/pdb{{ entry.rcsb_id }}/pdb
              </a>
            </p>
            <p>
              <span
                >Deposit Date:
                {{ formatDate(entry.rcsb_accession_info.deposit_date) }}</span
              >
              &nbsp;&nbsp;&nbsp;&nbsp;
              <span
                >Release Date:
                {{
                  formatDate(entry.rcsb_accession_info.initial_release_date)
                }}</span
              >
            </p>
            <p
              v-if="entry.pdbx_audit_support && entry.pdbx_audit_support.length"
            >
              Funding Organization:
              {{ entry.pdbx_audit_support[0].funding_organization }}
            </p>

            <p>
              Authors:
              <span v-for="author in entry.audit_author" :key="author.name">
                {{ author.name }}
                <span v-if="!$last">, </span>
              </span>
            </p>
          </div>
          <div v-else>
            <p>Loading...</p>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { fetchEntryDetails } from "../stores/graphqlClient";
export default {
  props: ["id"],
  data() {
    return {
      imageItems: [],
      entry: null,
    };
  },
  async mounted() {
    this.loadImages();
    try {
      const entries = await fetchEntryDetails(this.id);
      if (entries.length > 0) {
        this.entry = entries[0]; 
        console.log("Loaded entry:", this.entry);
      } else {
        console.warn("No entry found for ID:", this.id);
      }
    } catch (error) {
      console.error("Error fetching entry details:", error);
    }
  },
  // mounted() {
  //   this.loadImages();
  // },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    async loadImages() {
      let index = 1;
      const lowerCaseId = this.id.toLowerCase();
      const modelUrl = `https://cdn.rcsb.org/images/structures/${lowerCaseId}_model-1.jpeg`;
      // this.imageUrls.push(modelUrl);
      this.imageItems.push({ url: modelUrl, label: 'Model' });

      while (true) {
        const assemblyUrl = `https://cdn.rcsb.org/images/structures/${lowerCaseId}_assembly-${index}.jpeg`;
        const exists = await this.imageExists(assemblyUrl);
        if (exists) {
          // this.imageUrls.push(assemblyUrl);
          this.imageItems.push({ url: assemblyUrl, label: `Assembly-${index}` });
          index++;
        } else {
          break;
        }
      }
    
    },
    async imageExists(url) {
      try {
        const response = await fetch(url, { method: "HEAD" });
        return response.ok;
      } catch (error) {
        console.error("Error checking image:", error);
        return false;
      }
    },
  
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
}

.row {
  width: 100%;
}

.col-md-4,
.col-md-8 {
  padding: 0 15px;
}

/* .img-fluid {
  max-width: 100%;
  height: auto;
} */
.el-carousel__item {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
}

.carousel-item-content {
  position: relative;
  width: 100%;
  height: 300px; 
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.img-fluid {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.label {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
}

.el-carousel__item:nth-child(2n) {
  background-color: #ffffff;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #ffffff;
}
</style>

<!-- <template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-md-4">
        <img :src="structureImageUrl" alt="Protein Structure" class="w-100" />
      </div>
      <div class="col-md-8">
        <div v-if="entry">
          <p>PDB ID: {{ entry.rcsb_id }}</p>
          <p>Title: {{ entry.struct.title }}</p>
          <p>
            Initial Release Date:
            {{ entry.rcsb_accession_info.initial_release_date }}
          </p>
          <p>
            Authors:
            <span v-for="author in entry.audit_author" :key="author.name"
              >{{ author.name }}
              <span v-if="!$last">, </span>
            </span>
          </p>
          <p>
            PubMed ID: {{ entry.rcsb_primary_citation.pdbx_database_id_PubMed }}
          </p>
          <p>DOI: {{ entry.rcsb_primary_citation.pdbx_database_id_DOI }}</p>
        </div>
        <div v-else>
          <p>Loading...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchEntryDetails } from "../stores/graphqlClient";
export default {
  props: ["id"],
  data() {
    return {
      structureImageUrl:'https://cdn.rcsb.org/images/structures/6p64_assembly-1.jpeg',
      entry: null,
    };
  },
  async mounted() {
    try {
      this.entries = await fetchEntryDetails(this.id);
      this.entry = this.entries[0]; // 处理数组中的第一个元素
      console.log("Loaded entry:", this.entry);
    } catch (error) {
      console.error("Error fetching entry details:", error);
    }
  },
};
</script> -->

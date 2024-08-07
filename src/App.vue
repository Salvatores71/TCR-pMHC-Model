<template>
  <div id="app">
    <el-container>
      <el-header>
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" >
          <el-menu-item index="1" >
            <router-link  to="/" >Search PDB</router-link>
          </el-menu-item>
          <el-menu-item index="2" >
            <router-link  to="/results" >result</router-link>
          </el-menu-item>
          <el-menu-item index="3" >
            <router-link  to="/viewing" >Viewing</router-link>
          </el-menu-item>
          <el-menu-item index="4" >
            <router-link  to="/details/:id" >details</router-link>
          </el-menu-item>
        </el-menu>
      </el-header>

      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';
export default {
  data() {
    return {
      activeIndex: '1', 
    };
  },
  
}
</script>

<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  margin-top: 60px;
}

.el-header {
  /* background-color: #b3c0d1; */
  line-height: 60px;
}

.el-menu-demo {
  background-color: transparent;
}
</style>
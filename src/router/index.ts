import { createRouter, createWebHistory } from "vue-router";
import search from "../views/search.vue";
import viewing from "../views/viewing.vue";
import result from "../views/result.vue";
import PDBDetails from "../views/PDBDetails.vue"; 
import ThreeDViewer from "../views/3DViewer.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "search",
      component: search,
    },
    {
      path: "/viewing",
      name: "viewing",
      component: viewing,
    },
    {
      path: "/results",
      name: "result",
      component: result,
      props: true,
    },
    {
      path: "/details/:id",
      name: "PDBDetails",
      component: PDBDetails,
      props: true,
    },
    {
      path: "/3d-viewer",
      name: "3DViewer",
      component: ThreeDViewer,
      props: true,
    },
  ],
});

export default router;

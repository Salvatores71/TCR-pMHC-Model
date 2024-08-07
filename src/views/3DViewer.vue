<template>
  <div>
    <div
      id="gldiv"
      style="width: 100%; height: 80vh; margin: 0; padding: 0; border: 0"
    ></div>
    <hr style="margin: 0" />
    <br />
    <input type="button" value="Stick" @click="setStyle('stick')" />
    <input type="button" value="Line" @click="setStyle('line')" />
    <input type="button" value="Cross" @click="setStyle('cross')" />
    <input type="button" value="Sphere" @click="setStyle('sphere')" />
    <input type="button" value="Cartoon" @click="setStyle('cartoon')" />
    <br />
    <input type="button" value="addLabel" @click="addLabels" />
    <input type="button" value="removeLabel" @click="removeLabels" />
    <input type="button" value="Color SS" @click="colorSS" />
    <br />
    <input type="button" value="Surface1" @click="addSurface1" />
    <input type="button" value="Surface2" @click="addSurface2" />
    <input type="button" value="RM Surfaces" @click="removeSurfaces" />
    <br />
    <input type="button" value="Recenter" @click="recenter" />
    <br />
    <button @click="downloadPdb">Download</button>
    <br />
    <input type="file" @change="handleFileUpload" />
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { usePdbStore } from "../stores/pdbStore";

export default {
  setup() {
    const glviewer = ref(null);
    const pdbStore = usePdbStore();

    const setStyle = (style) => {
      const styles = {
        stick: { stick: {} },
        line: { line: {} },
        cross: { cross: { linewidth: 2 } },
        sphere: { sphere: {} },
        cartoon: { cartoon: {} },
      };
      if (glviewer.value) {
        glviewer.value.setStyle({}, styles[style]);
        glviewer.value.render();
      }
    };

    const addLabels = () => {
      if (glviewer.value) {
        const atoms = glviewer.value.getModel().selectedAtoms({ atom: "CA" });
        atoms.forEach((atom) => {
          const label = glviewer.value.addLabel(`${atom.resn} ${atom.resi}`, {
            inFront: true,
            fontSize: 12,
            position: { x: atom.x, y: atom.y, z: atom.z },
          });
          atom.label = label;
        });
        glviewer.value.render();
      }
    };

    const removeLabels = () => {
      if (glviewer.value) {
        const atoms = glviewer.value.getModel().selectedAtoms({ atom: "CA" });
        atoms.forEach((atom) => {
          if (atom.label) {
            glviewer.value.removeLabel(atom.label);
            delete atom.label;
          }
        });
        glviewer.value.render();
      }
    };

    const colorSS = () => {
      if (glviewer.value) {
        const m = glviewer.value.getModel();
        m.setColorByFunction({}, (atom) => {
          if (atom.ss === "h") return "magenta";
          if (atom.ss === "s") return "orange";
          return "white";
        });
        glviewer.value.render();
      }
    };

    const addSurface1 = () => {
      if (glviewer.value) {
        glviewer.value.addSurface(
          $3Dmol.SurfaceType.VDW,
          {},
          { hetflag: false, chain: "A" },
          { hetflag: false, chain: "A" }
        );
      }
    };

    const addSurface2 = () => {
      if (glviewer.value) {
        glviewer.value.addSurface(
          $3Dmol.SurfaceType.MS,
          {
            map: {
              prop: "partialCharge",
              scheme: new $3Dmol.Gradient.RWB(-0.6, 0.6),
            },
            opacity: 0.85,
          },
          { chain: "B" },
          { chain: "B" }
        );
      }
    };

    const removeSurfaces = () => {
      if (glviewer.value) {
        glviewer.value.removeAllSurfaces();
        // glviewer.value.removeLabel()
      }
    };

    const recenter = () => {
      if (glviewer.value) {
        glviewer.value.zoomTo();
      }
    };

    const downloadPdb = () => {
      if (glviewer.value) {
        glviewer.value.clear();
        $3Dmol.download(`pdb:${pdbStore.pdbId}`, glviewer.value, {
          doAssembly: true,
          noSecondaryStructure: false,
        });
      }
    };

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (evt) => {
        if (glviewer.value) {
          glviewer.value.clear();
          glviewer.value.addModel(evt.target.result, file.name);
          glviewer.value.zoomTo();
          glviewer.value.render();
        }
      };
      reader.readAsText(file);
    };

    onMounted(() => {
      const element = document.getElementById("gldiv");
      if (element) {
        glviewer.value = new $3Dmol.createViewer(element, {
          defaultcolors: $3Dmol.rasmolElementColors,
          // controls: {
          //   zoom: true, // 启用缩放
          //   pan: true, // 启用平移
          //   rotate: true, // 启用旋转
          // },
        });
        glviewer.value.setBackgroundColor(0xffffff);

        const pdbId = pdbStore.pdbId; // 获取 PDB ID
        const pdbUri = `../../server/downloads/${pdbId}.pdb`; // 构造文件路径

        $.ajax({
          url: pdbUri,
          success: function (data) {
            glviewer.value.addModel(data, "pdb");
            glviewer.value.zoomTo();
            glviewer.value.render();
          },
          error: function (xhr, status, err) {
            console.error(`Failed to load PDB file from ${pdbUri}`, err);
            alert("Failed to load the 3D structure.");
          },
        });
      }
    });

    return {
      glviewer,
      pdbStore,
      setStyle,
      addLabels,
      removeLabels,
      colorSS,
      addSurface1,
      addSurface2,
      removeSurfaces,
      recenter,
      downloadPdb,
      handleFileUpload,
    };
  },
};
</script>


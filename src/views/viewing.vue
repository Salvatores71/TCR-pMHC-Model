<template>
  <div>
    <div id="gldiv" style="width: 100%; height: 80vh; margin: 0; padding: 0; border: 0;"></div>
    <hr style="margin: 0;">
    <br>
    <input type="button" value="Stick" @click="setStyle('stick')">
    <input type="button" value="Line" @click="setStyle('line')">
    <input type="button" value="Cross" @click="setStyle('cross')">
    <input type="button" value="Sphere" @click="setStyle('sphere')">
    <input type="button" value="Cartoon" @click="setStyle('cartoon')">
    <input type="button" value="Label alpha C's" @click="addLabels">
    <input type="button" value="Color SS" @click="colorSS">
    <br>
    <input type="button" value="Surface1" @click="addSurface1">
    <input type="button" value="Surface2" @click="addSurface2">
    <input type="button" value="RM Surfaces" @click="removeSurfaces">
    <br>
    <input type="button" value="Recenter" @click="recenter">
    <br>
    <input v-model="pdbId" size="4">
    <button @click="downloadPdb">Download</button>
    <br>
    <input type="file" @change="handleFileUpload">
  </div>
</template>

<script>
export default {
  data() {
    return {
      glviewer: null,
      pdbId: '1UBQ'
    };
  },
  methods: {
    setStyle(style) {
      const styles = {
        stick: { stick: {} },
        line: { line: {} },
        cross: { cross: { linewidth: 2 } },
        sphere: { sphere: {} },
        cartoon: { cartoon: {} }
      };
      this.glviewer.setStyle({}, styles[style]);
      this.glviewer.render();
    },
    addLabels() {
      const atoms = this.glviewer.getModel().selectedAtoms({ atom: "CA" });
      atoms.forEach(atom => {
        const label = this.glviewer.addLabel(
          `${atom.resn} ${atom.resi}`,
          { inFront: true, fontSize: 12, position: { x: atom.x, y: atom.y, z: atom.z } }
        );
        atom.label = label;
      });
      this.glviewer.render();
    },
    colorSS() {
      const m = this.glviewer.getModel();
      m.setColorByFunction({}, atom => {
        if (atom.ss === 'h') return "magenta";
        if (atom.ss === 's') return "orange";
        return "white";
      });
      this.glviewer.render();
    },
    addSurface1() {
      this.glviewer.addSurface(
        $3Dmol.SurfaceType.VDW, {}, { hetflag: false, chain: 'A' }, { hetflag: false, chain: 'A' }
      );
    },
    addSurface2() {
      this.glviewer.addSurface(
        $3Dmol.SurfaceType.MS, { map: { prop: 'partialCharge', scheme: new $3Dmol.Gradient.RWB(-0.6, 0.6) }, opacity: 0.85 },
        { chain: 'B' }, { chain: 'B' }
      );
    },
    removeSurfaces() {
      this.glviewer.removeAllSurfaces();
    },
    recenter() {
      this.glviewer.zoomTo();
    },
    downloadPdb() {
      this.glviewer.clear();
      $3Dmol.download(`pdb:${this.pdbId}`, this.glviewer, { doAssembly: true, noSecondaryStructure: false });
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (evt) => {
        this.glviewer.clear();
        this.glviewer.addModel(evt.target.result, file.name);
        this.glviewer.zoomTo();
        this.glviewer.render();
      };
      reader.readAsText(file);
    }
  },
  mounted() {
    this.glviewer = new $3Dmol.createViewer("gldiv", {
      defaultcolors: $3Dmol.rasmolElementColors
    });
    this.glviewer.setBackgroundColor(0xffffff);
  }
};
</script>

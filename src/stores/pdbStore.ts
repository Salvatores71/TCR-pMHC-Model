import { defineStore } from 'pinia';

export const usePdbStore = defineStore('pdb', {
  state: () => ({
    pdbId: null as string | null,
  }),
  actions: {
    setPdbId(id:string) {
      this.pdbId = id;
    },
  },
});
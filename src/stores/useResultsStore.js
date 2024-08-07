
import { defineStore } from 'pinia';

export const useResultsStore = defineStore('resultsStore', {
  state: () => ({
    results: []
  }),
  actions: {
    setResults(newResults) {
      this.results = newResults;
    },
    clearResults() {
      this.results = [];
    }
  }
});
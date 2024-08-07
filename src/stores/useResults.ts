import { defineStore } from 'pinia';

interface Result {
  model_id: string;
  sequence: string;
  score: number;
  picture: string;
  download: string;
}

interface ResultsState {
  isLoading: boolean;
  results: Result[];
  error: string | null;
}

export const useResultsStore = defineStore('resultsStore', {
  state: (): ResultsState => ({
    isLoading: false,
    results: [],
    error: null
  }),
  actions: {
    setResults(newResults: Result[]) {
      this.results = newResults;
    },
    clearResults() {
      this.results = [];
    },
    setIsLoading(loading: boolean) {
      this.isLoading = loading;
    },
    setError(error: string | null) {
      this.error = error;
    }
  }
});
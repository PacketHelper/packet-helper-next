import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    showAlert: false,
  },
  mutations: {
    showAlert(state) {
      state.showAlert = true;
    },
    hideAlert(state) {
      state.showAlert = false;
    },
  },
  getters: {
    getVote(state) {
      return state.voted;
    },
    getAlert(state) {
      return state.showAlert;
    },
  },
});

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {},
  state: {
    voted: false,
    showPrompt: false
  },
  mutations: {
    togglePrompt(state) {
      state.showPrompt = !state.showPrompt
    },
    reset(state) {
      state.showPrompt = false
      state.voted = false
    },
    vote(state) {
      state.voted = true
    }
  },
  getters: {
    getVote(state) {
      return state.voted
    },
    getPrompt(state) {
      return state.showPrompt
    }
  }
})
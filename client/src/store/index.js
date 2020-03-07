import Vue from 'vue'
import Vuex from 'vuex'
import Axios from 'axios'
import socketStore from './modules/socket-store'

Vue.use(Vuex);

export const store = new Vuex.Store({
  modules: {
    socketStore
  },
})

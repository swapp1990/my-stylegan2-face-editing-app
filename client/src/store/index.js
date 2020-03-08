import Vue from 'vue'
import Vuex from 'vuex'
import Axios from 'axios'
import socketStore from './modules/socket-store'
import VueAnalytics from 'vue-analytics'

Vue.use(Vuex);
Vue.use(VueAnalytics, {
  id: 'UA-102725900-1'
});

export const store = new Vuex.Store({
  modules: {
    socketStore
  },
})

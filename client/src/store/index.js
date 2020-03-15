import Vue from 'vue'
import Vuex from 'vuex'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Axios from 'axios'
import socketStore from './modules/socket-store'
import VueAnalytics from 'vue-analytics'

Vue.use(Vuex);
Vue.use(VueAnalytics, {
  id: 'UA-102725900-1'
});
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

export const store = new Vuex.Store({
  modules: {
    socketStore
  },
})

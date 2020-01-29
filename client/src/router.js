import Vue from 'vue';
import Router from 'vue-router';

import FaceEditView from './views/FaceEditing.vue';
import FaceEditingUI from './views/FaceEditingNiceUI.vue';
import circleMenu from './views/CircularMenu.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: circleMenu
    }
  ],
});
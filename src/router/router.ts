import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import InfoWindow from "@/views/pages/InfoWindow.vue";
import MainPage from "@/views/pages/MainPage.vue";
import CreatorPage from "@/views/pages/CreatorPage.vue";
import SimpleDiffPage from "@/views/pages/SimpleDiffPage.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "home",
    component: MainPage,
  },
  {
    path: "/hex/",
    name: "home_hex",
    component: MainPage,
  },
  {
    path: "/hex/:hex_string",
    name: "hex",
    component: MainPage,
  },
  {
    path: "/info",
    name: "info",
    component: InfoWindow,
  },
  {
    path: "/creator",
    name: "creator",
    component: CreatorPage,
  },
  {
    path: "/compare",
    name: "compare",
    component: SimpleDiffPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;

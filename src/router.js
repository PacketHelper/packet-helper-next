import Vue from "vue";
import VueRouter from "vue-router";
import Info from "@/components/Info";
import LandingPage from "@/components/LandingPage";
import Creator from "@/components/Creator.vue";

Vue.use(VueRouter);

export default new VueRouter({
  routes: [
    {
      path: "/",
      name: "home",
      component: LandingPage,
    },
    {
      path: "/hex/",
      name: "home_hex",
      component: LandingPage,
    },
    {
      path: "/hex/:hex_string/like",
      name: "hex_like",
      component: LandingPage,
    },
    {
      path: "/hex/:hex_string/dislike",
      name: "hex_dislike",
      component: LandingPage,
    },
    {
      path: "/hex/:hex_string",
      name: "hex",
      component: LandingPage,
    },
    {
      path: "/info",
      name: "info",
      component: Info,
    },
    {
      path: "/creator",
      name: "creator",
      component: Creator,
    },
  ],
  mode: "history",
  hash: false,
});

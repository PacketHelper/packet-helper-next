import Vue from "vue";
import VueRouter from "vue-router";
import Info from "@/components/Info";
import LandingPage from "@/components/LandingPage";
import Creator from "@/components/Creator.vue";
import Compare from "@/components/Compare.vue";

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
    {
      path: "/compare",
      name: "compare",
      component: Compare,
    },
  ],
  mode: "history",
  hash: false,
});

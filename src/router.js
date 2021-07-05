import Vue from 'vue'
import VueRouter from 'vue-router'
// import VueDemo from '@/components/VueDemo'
import Messages from '@/components/Messages'
import Info from "@/components/Info";
import LandingPage from "@/components/LandingPage";
import Testing from "@/components/Testing.vue"

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingPage
    },
    {
      path: "/hex/",
      name: "home_hex",
      component: LandingPage
    },
    {
      path: '/hex/:hex_string',
      name: 'hex',
      component: LandingPage
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages
    },
    {
      path: "/info",
      name: "info",
      component: Info
    },
    {
      path: "/testing",
      name: "testing",
      component: Testing
    }
  ],
  mode: "history",
  hash: false
})

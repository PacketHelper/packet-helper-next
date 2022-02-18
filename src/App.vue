<template>
  <div id="app">
    <v-app>
      <AppBar />
      <v-main>
        <!-- Provides the application the proper gutter -->
        <v-container fluid>
          <v-container>
            <v-alert icon="mdi-shield-lock-outline" prominent text type="info">
              <strong>Legacy version</strong> of the PacketHelper is available
              at
              <a href="http://legacy.packethelper.com"
                >http://legacy.packethelper.com
              </a>
            </v-alert>
            <!-- If using vue-router -->
            <transition name="route" mode="out-in">
              <router-view> </router-view>
            </transition>
          </v-container>
        </v-container>
      </v-main>
    </v-app>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import AppBar from "@/components/AppBar.vue";

@Component({
  components: {
    AppBar,
  },
})
export default class App extends Vue {}
</script>

<style>
a {
  text-decoration: none;
}
.route-enter {
  opacity: 0;
  transform: translateX(-200px);
}
.route-enter-active {
  transition: all 0.3s ease-out;
}
.route-leave-to {
  opacity: 0;
  transform: translateX(200px);
}
.route-leave-active {
  transition: all 0.3s ease-in;
}
</style>

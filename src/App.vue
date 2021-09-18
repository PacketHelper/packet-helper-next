<template>
  <div id="app">
    <v-app>
      <v-app-bar dark app>
        <v-container>
          <v-toolbar>
            <v-toolbar-title
              >Packet helper
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <span v-bind="attrs" v-on="on">
                    <small id="version"
                      ><small>{{ version }}</small></small
                    ></span
                  >
                </template>
                <span
                  ><small>{{ revision }}</small></span
                >
              </v-tooltip>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <router-link to="/"><v-btn text>Decode</v-btn></router-link>
            <router-link to="/compare"
              ><v-btn text
                ><v-badge color="red" content="New">Simple Diff</v-badge></v-btn
              ></router-link
            >
            <v-btn text disabled>Visual</v-btn>
            <router-link to="/creator"
              ><v-btn text
                ><v-badge content="Preview">Creator</v-badge></v-btn
              ></router-link
            >
            <v-spacer></v-spacer>
            <v-btn text disabled
              >"Craft packets before, packets craft you" 🐱‍👤
            </v-btn>
          </v-toolbar>
        </v-container>
      </v-app-bar>

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

<script>
import ApiService from "@/services/apiService";

export default {
  name: "Info",
  data() {
    return {
      version: 0,
      revision: "dev",
    };
  },
  methods: {
    async getInfo() {
      const info = await ApiService.getInfo();
      this.version = info["version"];
      this.revision = info["revision"];
    },
  },
  mounted() {
    this.getInfo();
  },
};
</script>

<style>
#version {
  color: grey;
}
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

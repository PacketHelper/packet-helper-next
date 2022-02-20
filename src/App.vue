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
            <!-- <v-btn text disabled>Visual</v-btn> -->
            <router-link to="/creator"
              ><v-btn text
                ><v-badge content="Preview">Creator</v-badge></v-btn
              ></router-link
            >
            <v-spacer></v-spacer>
            <v-btn text disabled
              >"Craft packets before, packets craft you" 🐱‍👤
            </v-btn>
            <v-dialog v-model="dialog" width="500">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="grey" v-bind="attrs" v-on="on">
                  mdi-help-circle
                </v-icon>
              </template>

              <v-card>
                <v-card-title> About PacketHelper.com </v-card-title>
                <v-card-subtitle>
                  "Craft packets before, packets craft you" 🐱‍👤
                </v-card-subtitle>
                <v-card-text>
                  The application has been prepared to facilitate the work of
                  all those who work with internet packages on a daily basis. If
                  you program in P4 Lang at your work, use the PTF framework or
                  you don't know what happened to your package during the
                  laboratories at the university.
                  <br /><br />Find us at:<br />
                  <a href="https://github.com/PacketHelper/packet-helper-next"
                    ><v-icon>mdi-github</v-icon> GitHub
                    PacketHelper/packet-helper-next</a
                  >
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-card-text>{{ this.revision }}</v-card-text>
                  <v-btn text :href="this.getLinkToLatestRelease()">
                    Latest version {{ this.version }}
                  </v-btn>
                  <v-btn color="primary" text @click="dialog = false">
                    Close
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
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
      dialog: false,
    };
  },
  methods: {
    async getInfo() {
      const info = await ApiService.getInfo();
      this.version = info["version"];
      this.revision = info["revision"];
    },
    getLinkToLatestRelease() {
      if (this.version === 0) {
        return "https://github.com/PacketHelper/packet-helper-next";
      }
      return (
        "https://github.com/PacketHelper/packet-helper-next/releases/tag/" +
        this.version
      );
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
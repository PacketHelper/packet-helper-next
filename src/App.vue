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
            <v-btn text>Decode</v-btn>
            <v-btn text disabled>Diff</v-btn>
            <v-btn text disabled>Visual</v-btn>
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
              <strong>Paste a hex & click decode!</strong> Packet Helper is an
              online tool to analyze packet base on the hex information. Provide
              a hexdump information into text area and click "Decode". Spaces &
              new lines will be ignored.
            </v-alert>
            <!-- If using vue-router -->
            <router-view></router-view>
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
</style>

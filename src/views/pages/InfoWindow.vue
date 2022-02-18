<template>
  <div>
    <v-card>
      <v-card-title>Info</v-card-title>
      <v-card-text>
        Version: {{ this.version }}<br />
        Revision: {{ this.revision }}
      </v-card-text>
      <v-card-actions>
        <v-btn text> LinkedIn </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import MessageService from "@/services/apiService";

@Component
export default class Info extends Vue {
  version = "0";
  revision = "dev";

  async getInfo(): Promise<void> {
    const info = await MessageService.getInfo();
    this.version = info["version"];
    this.revision = info["revision"];
  }

  mounted(): void {
    this.getInfo();
  }
}
</script>

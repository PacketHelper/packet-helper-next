<template>
  <div>
    <v-card>
      <v-card-title>Info</v-card-title>
      <v-card-text>
        Version: {{ this.version }}<br>
        Revision: {{ this.revision }}
      </v-card-text>
      <v-card-actions>
        <v-btn text>
          LinkedIn
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import MessageService from "../services/messageService";

export default {
  name: "Info",
  data() {
    return {
      version: 0,
      revision: "dev"
    }
  },
  methods: {
    async getInfo() {
      const info = await MessageService.getInfo();
      this.version = info["version"];
      this.revision = info["revision"];
    }
  },
  mounted() {
    this.getInfo();
  }
}
</script>

<style>

</style>
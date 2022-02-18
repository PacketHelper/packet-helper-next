<template>
  <div>
    <div class="share" v-if="struct.length > 0">
      <v-btn
        elevation="6"
        dark
        large
        color="blue"
        @click="handleCopy"
        class="shareBtn"
      >
        <v-icon>mdi-content-copy</v-icon> Copy link
      </v-btn>
    </div>
    <v-snackbar v-model="snackbar" color="green dark-2" :timeout="timeout">
      <h2>👌 Link has been copied</h2>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class ShareButton extends Vue {
  @Prop() struct!: any;
  snackbar = false;
  timeout = 3000;

  async handleCopy() {
    await navigator.clipboard.writeText(this.getActualPath());
    this.snackbar = !this.snackbar;
  }

  getActualPath(): string {
    return `https://www.packethelper.com${this.$route.fullPath}`;
  }
}
</script>

<style>
.share {
  position: fixed;
  top: 94vh;
  right: 1rem;
  z-index: 1;
}
</style>

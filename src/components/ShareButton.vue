<template>
  <div>
    <transition-group
      @before-enter="slideBefore"
      @enter="slideEnter"
      @leave="slideLeave"
      mode="out-in"
      appear
      tag="div"
    >
      <div class="share" :key="0" v-if="struct.length > 0">
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
    </transition-group>
    <Toast type="success" :trigger="sw" :key="0">
      <template #info> Link has been copied </template>
    </Toast>
  </div>
</template>

<script>
import gsap from "gsap";
import Toast from "./Toast.vue";

export default {
  props: ["data", "struct"],
  components: { Toast },
  data() {
    return {
      link: "next.packethelper.com" + this.$route.fullPath,
      sw: 0,
    };
  },
  methods: {
    async handleCopy() {
      await navigator.clipboard.writeText(this.link);
      this.sw = !this.sw;
    },
    slideBefore(el) {
      el.style.transform = "translateX(250px)";
      el.style.opacity = "0";
    },
    slideEnter(el, done) {
      gsap.to(el, {
        x: 0,
        opacity: 1,
        duration: 0.5,
        onComplete: done,
      });
    },
    slideLeave(el, done) {
      gsap.to(el, {
        x: 250,
        opacity: 0,
        duration: 0.5,
        delay: 0.5,
        onComplete: done,
      });
    },
  },
  watch: {
    "$route.fullPath": function () {
      this.link = "next.packethelper.com" + this.$route.fullPath;
    },
  },
};
</script>

<style>
.share {
  position: fixed;
  top: 94vh;
  right: 1rem;
  z-index: 1;
}
</style>

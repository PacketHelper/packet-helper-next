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
    <transition-group @enter="slide2Enter" @leave="slide2Leave">
      <div class="alert" v-if="alert" :key="1">
        <v-alert border="left" type="success" width="300px"
          ><div class="closeWindow" @click="handleClose">
            <v-icon>mdi-close</v-icon>
          </div>
          Link has been copied
          <div class="progress">
            <v-progress-linear
              class="progress"
              :value="time"
              color="error"
            ></v-progress-linear>
          </div>
        </v-alert>
      </div>
    </transition-group>
  </div>
</template>

<script>
import gsap from "gsap";
export default {
  props: ["data", "struct"],
  data() {
    return {
      link: "next.packethelper.com" + this.$route.fullPath,
      time: 0,
      inter: null,
    };
  },
  methods: {
    async handleCopy() {
      await navigator.clipboard.writeText(this.link);
      this.time = 110;
      // Starts timer when alert is hidden
      if (!this.$store.getters.getAlert) {
        this.inter = setInterval(() => {
          this.time -= 5;
          if (this.time < -20) {
            clearInterval(this.inter);
            this.$store.commit("hideAlert");
          }
        }, 100);
      }
      this.$store.commit("showAlert");
    },
    handleClose() {
      this.$store.commit("hideAlert");
      clearInterval(this.inter);
    },
    slideBefore(el) {
      el.style.transform = "translateX(200px)";
    },
    slideEnter(el, done) {
      gsap.to(el, {
        x: 0,
        duration: 0.5,
        onComplete: done,
      });
    },
    slideLeave(el, done) {
      gsap.to(el, {
        x: 200,
        duration: 0.5,
        delay: 0.5,
        onComplete: done,
      });
    },
    slide2Enter(el, done) {
      gsap.to(el, {
        y: 0,
        duration: 0.4,
        onComplete: done,
      });
    },
    slide2Leave(el, done) {
      gsap.to(el, {
        y: 200,
        duration: 0.4,
        onComplete: done,
      });
    },
  },
  computed: {
    alert() {
      return this.$store.getters.getAlert;
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
.alert {
  z-index: 0;
  position: fixed;
  transform: translateY(200px);
  top: 87vh;
  right: 50rem;
}
.progress {
  margin: 0px -42px 0px -27px;
  padding: 0px;
  top: 16px;
}
.closeWindow {
  position: fixed;
  right: 0.2rem;
  cursor: pointer;
}
</style>

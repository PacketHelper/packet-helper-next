<template>
  <transition-group @enter="slide2Enter" @leave="slide2Leave">
    <div v-if="alert1" class="alert" :key="1">
      <v-alert border="left" :type="type" width="300px"
        ><div class="closeWindow" @click="handleClose">
          <v-icon>mdi-close</v-icon>
        </div>
        <slot name="info"></slot>
        <div class="progress">
          <v-progress-linear
            class="progress"
            :value="time"
            color="indigo"
          ></v-progress-linear>
        </div>
      </v-alert>
    </div>
  </transition-group>
</template>

<script>
import gsap from "gsap";

export default {
  props: ["type", "trigger"],
  data() {
    return {
      inter: null,
      time: 0,
      alert1: 0,
    };
  },
  methods: {
    timer() {
      this.time = 110;
      // Starts timer when alert is hidden
      if (!this.$store.getters.getAlert) {
        this.inter = setInterval(() => {
          this.time -= 5;
          if (this.time < -20) {
            clearInterval(this.inter);
            this.alert1 = false;
          }
        }, 100);
      }
      this.alert1 = true;
    },
    handleClose() {
      this.alert1 = false;
      clearInterval(this.inter);
    },
    slide2Enter(el, done) {
      gsap.to(el, {
        y: 0,
        duration: 0.3,
        onComplete: done,
      });
    },
    slide2Leave(el, done) {
      gsap.to(el, {
        y: 200,
        duration: 0.3,
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
    trigger: function () {
      this.timer();
    },
  },
};
</script>

<style>
.alert {
  z-index: 0;
  position: fixed;
  transform: translateY(200px);
  top: 89vh;
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
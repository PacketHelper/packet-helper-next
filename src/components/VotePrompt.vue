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
      <div
        class="feedback"
        :key="0"
        v-if="(!hasVoted || prompt) && struct.length > 0"
      >
        <v-btn
          elevation="6"
          dark
          fab
          large
          color="blue"
          @click="showPrompt"
          class="feedbackBtn"
        >
          <v-icon>mdi-thumb-up</v-icon>
        </v-btn>
      </div>
    </transition-group>
    <transition-group @enter="popupEnter" @leave="popupLeave">
      <div class="prompt" v-if="prompt && struct.length > 0" :key="0">
        <div v-if="!hasVoted">
          <div class="prompt-text">Was this packet decoded properly?</div>
          <v-btn class="vote" @click="vote(true)">
            <v-icon text icon color="green lighten-1"> mdi-thumb-up </v-icon>
          </v-btn>
          <v-btn class="vote" @click="vote(false)">
            <v-icon text icon color="red lighten-2"> mdi-thumb-down </v-icon>
          </v-btn>
        </div>
        <div v-else class="voted">
          <p>Thanks for feedback!</p>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script>
import gsap from "gsap";

export default {
  props: ["data", "struct"],
  methods: {
    vote(result) {
      this.$store.commit("vote");
      let hexPacket = this.data;
      // Place for API call
      // To refrence hex value use hexPacket
      // Result argument stores a boolean value
      console.log(hexPacket);
      console.log(result);
    },
    showPrompt() {
      console.log(this.$store.getters.getPrompt);
      this.$store.commit("togglePrompt");
    },
    slideBefore(el) {
      el.style.transform = "translateX(100px)";
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
        x: 100,
        duration: 0.5,
        delay: 0.5,
        onComplete: done,
      });
    },
    popupBefore(el) {
      el.style.transform = "scale(0)";
    },
    popupEnter(el, done) {
      gsap.to(el, {
        scale: 1,
        duration: 0.4,
        onComplete: done,
      });
    },
    popupLeave(el, done) {
      gsap.to(el, {
        scale: 0,
        duration: 0.4,
        onComplete: done,
      });
    },
    delay(seconds) {
      return new Promise((res) => setTimeout(res, seconds * 1000));
    },
  },
  computed: {
    hasVoted() {
      return this.$store.getters.getVote;
    },
    prompt() {
      return this.$store.getters.getPrompt;
    },
  },
};
</script>

<style>
.rating {
  text-align: center;
  margin-top: 0.15rem;
}
.vote {
  margin: 0 5px 10px 5px;
}
.feedback {
  position: fixed;
  top: 88vh;
  right: 1rem;
  z-index: 1;
}
.prompt {
  z-index: 0;
  text-align: center;
  overflow: hidden;
  background: #2196f3;
  height: 100px;
  width: 300px;
  position: fixed;
  top: 83vh;
  right: 1.9rem;
  transform-origin: bottom right;
  transform: scale(0);
  border-radius: 8px;
  color: white;
  font-family: monospace, monospace;
}

.voted {
  padding: 37px;
}
.prompt-text {
  font-size: 13px;
  padding-top: 15px;
  padding-bottom: 10px;
}
</style>
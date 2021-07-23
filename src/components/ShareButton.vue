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
      <div class="feedback" :key="0" v-if="struct.length > 0">
        <v-btn
          elevation="6"
          dark
          fab
          large
          color="blue"
          @click="showPrompt"
          class="feedbackBtn"
        >
          <v-icon>fa-share</v-icon>
        </v-btn>
      </div>
    </transition-group>
    <transition-group @enter="popupEnter" @leave="popupLeave">
      <div class="prompt" v-if="prompt" :key="1">
        <div class="shareTitle">Share this packet</div>
        <div class="shareLabel">Share link</div>
        <div class="shareprompt">
          <v-text-field
            solo
            dense
            outlined
            readonly
            background-color="#ddd"
            label="Link to share"
            :value="link"
          ></v-text-field>
        </div>
        <div class="copyBtn">
          <v-btn outlined height="30px" @click="copy" width="130px"
            ><div v-if="!copied">Copy link</div>
            <v-icon v-else color="green">mdi-check</v-icon></v-btn
          >
        </div>
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
      link: "next.packet-helper.com" + this.$route.fullPath,
      copied: false,
    };
  },
  methods: {
    showPrompt() {
      console.log(this.link);
      this.$store.commit("togglePrompt");
      this.copied = false;
    },
    async copy(el) {
      await navigator.clipboard.writeText(this.link);
      this.copied = true;
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
  height: 150px;
  width: 400px;
  position: fixed;
  top: 78vh;
  right: 1.9rem;
  transform-origin: bottom right;
  transform: scale(0);
  border-radius: 8px;
  font-family: monospace, monospace;
  border: 1px solid;
  background: white;
}
.voted {
  padding: 37px;
}
.prompt-text {
  font-size: 13px;
  padding-top: 15px;
  padding-bottom: 10px;
}
.shareprompt {
  display: flex;
  padding: 5px 5px 0 5px;
}
.copyBtn {
  text-align: left;
  margin-top: -20px;
  padding-left: 5px;
  padding-top: 5px;
}
.shareLabel {
  text-align: right;
  padding-right: 10px;
  margin-bottom: -8px;
  font-size: 14px;
}
.shareTitle {
  padding-top: 6px;
}
</style>

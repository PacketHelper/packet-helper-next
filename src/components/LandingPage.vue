<template>
  <div>
    <v-container>
      <v-card elevation="6">
        <v-card-title>Decode Packet</v-card-title>
        <v-card-text>
          <v-textarea id="hex" solo label="Hex" v-model="hexValue"></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn
            class="white--text"
            color="warning"
            depressed
            large
            @click="cleanHex"
          >
            Clean hex
          </v-btn>
          <v-btn color="primary" @click="goToHex" large>Decode</v-btn>
          <v-btn text @click="reset">Reset</v-btn>
          <v-spacer></v-spacer>
          <div v-if="structure">
            <transition
              @before-enter="beforeEnterButton"
              @enter="enterButton"
              @leave="leaveButton"
              mode="out-in"
            >
              <v-btn
                v-if="structure.length > 0 && !isExpanded"
                class="white--text"
                color="indigo"
                @click="expand"
              >
                Expand all
              </v-btn>
              <v-btn
                v-else-if="structure.length > 0"
                class="white--text"
                color="indigo"
                @click="collapse"
              >
                Collapse all
              </v-btn>
            </transition>
          </div>
          <v-btn text @click="showExamples">Next Example</v-btn>
        </v-card-actions>
      </v-card>
      <transition-group
        @before-enter="beforeEnterUp"
        @enter="enterUp"
        @leave="leaveUp"
        mode="out-in"
      >
        <v-card
          style="margin-top: 2rem"
          v-if="loading"
          :key="6"
          :data-index="6"
        >
          <v-card-title>Loading packet...</v-card-title>
          <v-card-subtitle>Loading</v-card-subtitle>
          <v-card-text class="text-center">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-card-text>
        </v-card>
        <v-alert
          v-else-if="alert"
          v-model="alert"
          border="left"
          type="error"
          close-text="Close Alert"
          dark
          dismissible
          :key="7"
        >
          Error: Can not properly decode the hex.
        </v-alert>
        <v-alert
          v-else-if="warning"
          v-model="warning"
          border="left"
          type="warning"
          close-text="Close Alert"
          dark
          dismissible
          :key="8"
        >
          Warning: This protocol is not officially supported and some of the
          data may be displayed incorrectly
        </v-alert>
      </transition-group>
      <div class="wrapper" v-if="structure">
        <v-expansion-panels
          multiple
          focusable
          style="margin-top: 1rem; width: auto; display: block"
          v-model="panel"
        >
          <transition-group
            @before-enter="beforeEnter"
            @enter="enter"
            @leave="leave"
            mode="out-in"
          >
            <v-card
              v-if="structure.length > 0"
              style="margin-top: 1rem"
              elevation="6"
              :key="0"
              :data-index="0"
            >
              <v-card-title>Packet summary</v-card-title>
              <v-card-subtitle>{{ header.join(" / ") }}</v-card-subtitle>
              <v-card-text>
                Length: {{ summary["length"] }}{{ summary["length_unit"] }}
                <v-textarea
                  id="hex"
                  filled
                  name="input-7-4"
                  label="Hexdump"
                  :value="summary['hexdump']"
                  auto-grow
                  readonly
                ></v-textarea>
              </v-card-text>
            </v-card>
            <Display
              v-for="(s, index) in structure"
              :key="index + 1"
              :data="s"
              :data-index="index + 1"
              @warning="handleWarning"
            ></Display>
          </transition-group>
        </v-expansion-panels>
      </div>
    <VotePrompt :data="hexValue" :struct="structure" :key="0"></VotePrompt>
    </v-container>
  </div>
</template>

<script>
import apiService from "../services/apiService.js";
import Display from "./Display.vue";
import DropDown from "./DropDown.vue";
import VotePrompt from "./VotePrompt.vue";
import gsap from "gsap";

export default {
  name: "LandingPage",
  components: { Display, DropDown, VotePrompt },
  data() {
    return {
      hexValue: "",
      decode: false,
      loading: false,
      structure: [],
      summary: [],
      header: [],
      alert: false,
      warning: false,
      panel: [],
      isExpanded: false,
      voted: false,
    };
  },
  methods: {
    goToHex() {
      this.hexValue = this.hexValue.replace(/\s/g, "");
      this.$router.replace(`/hex/${this.hexValue}`);
      this.showPacket();
      this.getPacket();
    },
    read() {
      if (this.$route.query["redirect"]) {
        this.hexValue = this.$route.query["redirect"];
        this.goToHex();
      } else {
        this.hexValue = this.$route.params.hex_string;
      }
      this.showPacket();
    },
    async reset() {
      this.hexValue = "";
      this.decode = false;
      this.resetData();
      this.$store.commit("reset");
      await this.delay(0.6);
      this.alert = false;
      this.loading = false;
      this.warning = false;
      this.voted = false;
      this.$router.replace("/hex/");
    },
    resetData() {
      this.summary = [];
      this.header = [];
      this.structure = [];
    },
    showPacket() {
      try {
        this.decode = this.hexValue.length > 0;
        // eslint-disable-next-line no-empty
      } catch (error) {}
    },
    async getPacket() {
      if (this.hexValue !== "undefined") {
        this.resetData();
        this.$store.commit("reset");
        await this.delay(0.6);
        this.loading = true;
        this.alert = false;
        this.warning = false;
        try {
          const hexResponse = await apiService.getHex(this.hexValue);
          this.structure = hexResponse["structure"];
          this.summary = hexResponse["summary"];
          if (this.structure.length === 0) {
            throw "Empty Structure";
          }
        } catch (err) {
          this.loading = false;
          this.alert = true;
          return;
        }
        this.loading = false;
        this.alert = false;
        this.packData();
      }
    },
    packData() {
      this.header = [];
      this.structure.forEach((packet) => {
        this.header.push(packet["name"]);
      });
    },
    cleanHex() {
      let value = this.hexValue.split(" ");

      // let slicePotentialHex = value.slice(2, 18)
      // let notHexFlag = slicePotentialHex.some(el => {
      //   return el.length !== 2;
      // });
      //
      // if (notHexFlag) {
      //   return false;
      // }
      let stack = [];
      let regex = new RegExp("[0-9a-fA-F]{1,2}");
      value.forEach((h) => {
        if (h.length === 2 && regex.test(h)) {
          stack.push(h);
        }
      });
      this.hexValue = stack.join(" ");
    },
    showExamples() {
      const example_array = [
        "ff ff ff aa a9 ff 00 00 00 00 00 12 08 00 45 00 00 3c 00 01 00 00 40 04 7c bb 7f 00 00 01 7f 00 00 01 45 00 00 28 00 01 00 00 40 06 7c cd 7f 00 00 01 7f 00 00 01 00 14 00 50 00 00 00 00 00 00 00 00 50 02 20 00 91 7c 00 00",
        "00 00 00 00 00 00 00 10 94 00 12 02 08 00 45 00 00 3D 00 0E 00 00 0A 11 2F 4A C0 55 01 02 C0 00 00 01 04 00 0E C8 00 29 72 31 20 44 05 21 00 00 00 01 00 00 00 00 00 0F 42 40 00 0F 42 40 00 00 00 00 01 09 02 73 65 63 72 65 74 FA 7B 79 1C",
        "00 00 1C ff ff ff 00 00 00 00 00 00 08 00 45 00 00 34 00 01 00 00 40 04 7c c3 7f 00 00 01 7f 00 00 01 45 00 00 20 00 01 00 00 40 2f 7c ac 7f 00 00 01 7f 00 00 01 00 00 00 00 00 35 00 35 00 08 00 00",
        "ff ff ff ff ff ff 00 00 00 00 00 00 08 00 45 00 00 48 00 01 00 00 40 29 7c 8a 7f 00 00 01 7f 00 00 01 60 00 00 00 00 0c 2f 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 35 00 35 00 08 00 00",
        "00 E0 1C CC CC C2 00 1F 33 D9 73 61 08 00 45 00 00 80 00 00 40 00 40 11 24 55 0A 0A 01 01 0A 0A 01 04 00 35 DB 66 00 6C 2D 2D 79 56 81 80 00 01 00 02 00 02 00 00 04 6D 61 69 6C 08 70 61 74 72 69 6F 74 73 02 69 6E 00 00 01 00 01 C0 0C 00 05 00 01 00 00 2A 4B 00 02 C0 11 C0 11 00 01 00 01 00 00 2A 4C 00 04 4A 35 8C 99 C0 11 00 02 00 01 00 01 43 8C 00 06 03 6E 73 32 C0 11 C0 11 00 02 00 01 00 01 43 8C 00 06 03 6E 73 31 C0 11",
        "ff ff ff ff ff ff 00 00 00 00 00 00 08 00 45 00 00 71 00 01 00 00 40 29 7c 61 7f 00 00 01 7f 00 00 01 60 00 00 00 00 35 2f 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 35 00 35 00 31 00 00 73 6f 6d 65 20 72 61 6e 64 6f 6d 20 73 74 72 69 6e 67 20 31 31 32 33 34 34 35 39 38 32 37 33 34 39 38 32 37 33 34 32 33 34",
      ];
      let r_value = Math.floor(Math.random() * example_array.length);
      this.hexValue = example_array[r_value];
    },
    delay(seconds) {
      return new Promise((res) => setTimeout(res, seconds * 1000));
    },
    handleWarning() {
      this.warning = true;
    },
    beforeEnter(el) {
      el.style.opacity = 0;
      el.style.transform = "translateY(100px)";
    },
    enter(el, done) {
      gsap.to(el, {
        opacity: 1,
        y: 3,
        duration: 0.6,
        onComplete: done,
        delay: el.dataset.index * 0.15 + 0.5,
      });
    },
    leave(el, done) {
      gsap.to(el, {
        opacity: 0,
        y: 100,
        duration: 0.25,
        onComplete: done,
        delay: (5 - el.dataset.index) * 0.06,
      });
    },
    beforeEnterUp(el) {
      el.style.opacity = 0;
      el.style.transform = "translateY(-40px)";
    },
    enterUp(el, done) {
      gsap.to(el, {
        opacity: 1,
        y: 3,
        duration: 0.4,
        onComplete: done,
        delay: 0.4,
      });
    },
    leaveUp(el, done) {
      gsap.to(el, {
        opacity: 0,
        y: -40,
        duration: 0.4,
        onComplete: done,
      });
    },
    beforeEnterButton(el) {
      el.style.opacity = 0;
      el.style.transform = "translateY(10px)";
    },
    enterButton(el) {
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 0.1,
      });
    },
    leaveButton(el) {
      gsap.to(el, {
        opacity: 0,
        y: 10,
        duration: 0.1,
      });
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
    expand() {
      this.panel = [...Array(this.structure.length).keys()];
      this.isExpanded = true;
    },
    collapse() {
      this.panel = [];
      this.isExpanded = false;
    },
  },
  mounted() {
    this.read();
    if (this.$route.fullPath === "/") {
      this.showExamples();
    } else {
      this.showPacket();
      this.getPacket();
    }
  },
  watch: {
    panel: function () {
      if (!this.panel.length) this.isExpanded = false;
      else if (this.panel.length === this.structure.length)
        this.isExpanded = true;
    },
  },
};
</script>

<style>
#hex {
  font-family: monospace, monospace;
}

.data {
  position: absolute;
}
</style>
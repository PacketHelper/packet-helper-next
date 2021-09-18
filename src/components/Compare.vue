<template>
  <div>
    <v-card>
      <v-card-title>Simple Compare</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              Hex A
              <v-card-text>
                <v-textarea
                  id="hexA"
                  solo
                  label="Hex A"
                  v-model="hexValueA"
                ></v-textarea>
                <v-btn @click="cleanHex('hexValueA')">Clean A</v-btn>
              </v-card-text>
            </v-col>
            <v-col>
              Hex B
              <v-card-text>
                <v-textarea
                  id="hexB"
                  solo
                  label="Hex B"
                  v-model="hexValueB"
                ></v-textarea>
                <v-btn @click="cleanHex('hexValueB')">Clean B</v-btn>
              </v-card-text>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-btn
          class="white--text"
          color="warning"
          depressed
          large
          @click="cleanHexs"
        >
          Clean hexs
        </v-btn>
        <v-btn color="primary" large>Quick diff</v-btn>
        <!-- <v-btn text @click="reset">Reset</v-btn> -->
        <!-- <v-checkbox
          v-model="expandOnLoad"
          :value="expandOnLoad"
          :label="`Expand on load?`"
        ></v-checkbox> -->
        <!-- <v-spacer></v-spacer>
        <v-btn text @click="showExamples">Next Example</v-btn> -->
      </v-card-actions>
    </v-card>
    <code-diff :old-string="hexValueA" :new-string="hexValueB" :context="10" />
  </div>
</template>

<script>
import MessageService from "../services/apiService";
import CodeDiff from 'vue-code-diff';

export default {
  name: "Compare",
  components: {CodeDiff},
  data() {
    return {
      hexValueA: "",
      hexValueB: "",
      prettyDiff: "",
    };
  },
  methods: {
    async getInfo() {
      const info = await MessageService.getInfo();
      this.version = info["version"];
      this.revision = info["revision"];
    },
    cleanHexs() {
      ["hexValueA", "hexValueB"].forEach(this.cleanHex);
    },
    cleanHex(potentialId) {
      console.log(potentialId);
      let value = this[potentialId].split(" ");

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
      this[potentialId] = stack.join(" ");
    },
    // diff() {
    //   let diff = new Diff();
    //   let text_diff = diff.main(this.hexValueA, this.hexValueB);
    //   this.prettyDiff = text_diff.prettyHtml(text_diff);
    // },
  },
  mounted() {
    this.getInfo();
  },
};
</script>

<style></style>

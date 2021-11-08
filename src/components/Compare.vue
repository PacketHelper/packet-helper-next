<template>
  <div>
    <v-card>
      <v-card-title>Simple Compare</v-card-title>
      <v-card-text>
        <v-container>
          The purpose of this view is to compare two packets to check for
          differences between them. It can be helpful in finding the difference
          between the outgoing packet and the packet received on the selected
          port.
          <v-tooltip v-model="show" top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon color="grey lighten-1"> mdi-help-circle </v-icon>
              </v-btn>
            </template>
            <span>
              Enter Hex A and Hex B to see the differences. If you copied your
              frame along with the information in `HEXDUMP`, use" Clean "first,
              then look for more information with" Refresh ". If both packages
              contain add-ons from the `HEXDUMP` function, use the" Clean & Show
              Diff "option. Otherwise, use "Quick diff". If something has
              changed, use "Refresh".</span
            >
          </v-tooltip>
          <br /><br />

          <v-row>
            <v-col>
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
          :loading="loading"
          :disabled="loading"
          large
          @click="cleanHexs"
        >
          Clean & show diff
        </v-btn>
        <v-btn
          color="primary"
          :loading="loading"
          :disabled="loading"
          @click="diff"
          large
          >Quick diff</v-btn
        >
      </v-card-actions>
    </v-card>
    <v-card
      v-if="hexValueA !== '' && hexValueB !== ''"
      style="margin-top: 1rem"
    >
      <v-card-title>Simple diff</v-card-title>
      <v-card-text>
        <code-diff
          :old-string="hexValueA.toUpperCase()"
          :new-string="hexValueB.toUpperCase()"
          :context="10"
        />
      </v-card-text>
    </v-card>

    <v-alert
      border="top"
      color="red lighten-2"
      dark
      v-if="hexValueA.length !== hexValueB.length"
      style="margin-top: 1rem"
    >
      The given frames vary in length ({{
        hexValueA.replace(/\s/g, "").length / 2
      }}B != {{ hexValueB.replace(/\s/g, "").length / 2 }}B). To avoid any
      problems, PacketHelper will show only the common part, please treat the
      rest as RAW data
    </v-alert>
    <v-card
      v-if="
        hexValueA.toLowerCase() !== '' &&
        hexValueB.toLowerCase() !== '' &&
        hexValueA.toLowerCase() !== hexValueB.toLowerCase()
      "
      style="margin-top: 1rem"
    >
      <v-card-title>More diff information</v-card-title>
      <v-card-text v-if="loading">
        <center>Loading...</center>
      </v-card-text>
      <v-card-text v-else>
        More information per structure:
        <ul>
          <li
            v-for="(item, index) in combined.slice(0, shorter())"
            :key="index"
          >
            {{ item[0]["name"] }} = {{ item[1]["name"] }}
            <div>
              <div v-if="item[0]['chksum_status']['status'] === true">
                A: ✔️ Chksum: {{ item[0]["chksum_status"]["chksum"] }}
              </div>
              <div v-else-if="item[0]['chksum_status']['status'] === false">
                A: ❌ Chksum: {{ item[0]["chksum_status"]["chksum"] }}; should
                be
                {{ item[0]["chksum_status"]["chksum_calculated"] }}
              </div>
              <div v-if="item[1]['chksum_status']['status'] === true">
                B: ✔️ Chksum: {{ item[1]["chksum_status"]["chksum"] }}
              </div>
              <div v-else-if="item[1]['chksum_status']['status'] === false">
                B: ❌ Chksum: {{ item[1]["chksum_status"]["chksum"] }}; should
                be
                {{ item[1]["chksum_status"]["chksum_calculated"] }}
              </div>
            </div>
            <code-diff
              :old-string="item[0]['repr']"
              :new-string="item[1]['repr']"
              :context="10"
            />
          </li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn
          class="ma-2"
          :loading="loading"
          :disabled="loading"
          color="secondary"
          @click="diff"
          large
          >Refresh <v-icon right dark> mdi-refresh </v-icon></v-btn
        >
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import MessageService from "../services/apiService";
import CodeDiff from "vue-code-diff";

export default {
  name: "Compare",
  components: { CodeDiff },
  data() {
    return {
      hexValueA: "",
      hexValueB: "",
      prettyDiff: "",
      structureA: [],
      structureB: [],
      combined: [],
      loading: false,
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
      this.diff();
    },
    cleanHex(potentialId) {
      let value = this[potentialId].split(" ");
      let stack = [];
      let regex = new RegExp("[0-9a-fA-F]{1,2}");

      value.forEach((h) => {
        if (h.length === 2 && regex.test(h)) {
          stack.push(h);
        }
      });
      this[potentialId] = stack.join(" ");
    },
    diff() {
      this.getPacket();
    },
    showDiffExample() {
      const example_array = [
        [
          "ff ff ff aa a9 ff 00 00 00 00 00 12 08 00 45 00 00 3c 00 01 00 00 40 04 7c bb 7f 00 00 01 7f 00 00 01 45 00 00 28 00 01 00 00 40 06 7c cd 7f 00 00 01 7f 00 00 01 00 14 00 50 00 00 00 00 00 00 00 00 50 02 20 00 91 7c 00 00",
          "ff ff ff bb a9 ff 00 00 00 00 00 12 08 00 45 00 00 3c 00 01 00 00 40 04 7c ab 7f 00 00 01 7f 00 00 01 45 00 00 28 00 01 00 00 40 06 7c cd 7f 00 00 01 7f 00 00 01 00 14 00 50 00 00 00 00 00 00 00 00 50 02 20 00 91 7c 00 00",
        ],
      ];
      let r_value = Math.floor(Math.random() * example_array.length);
      this.hexValueA = example_array[r_value][0];
      this.hexValueB = example_array[r_value][1];
    },
    shorter() {
      let lenA = this.structureA.length;
      let lenB = this.structureB.length;
      return Math.min(lenA, lenB);
    },
    async getPacket() {
      this.structureA = [];
      this.structureB = [];
      this.loading = true;

      if (this.hexValueA !== "undefined" || this.hexValueB !== "undefined") {
        try {
          const hexResponse = await MessageService.getHex(
            this.hexValueA.replace(/\s/g, "")
          );
          this.structureA = hexResponse["structure"];
          if (this.structureA.length === 0) {
            throw "Empty Structure";
          }
        } catch (err) {
          return;
        }

        try {
          const hexResponseB = await MessageService.getHex(
            this.hexValueB.replace(/\s/g, "")
          );
          this.structureB = hexResponseB["structure"];
          if (this.structureB.length === 0) {
            throw "Empty Structure";
          }
        } catch (err) {
          return;
        }

        let reprA = this.structureA.map((e, i) => {
          return e["repr"];
        });

        this.combined = this.structureA.map((e, i) => {
          try {
            return [e, this.structureB[i]];
          } catch (e) {
            this.loading = false; // TODO Extend this for alert message
          }
        });
        this.loading = false;
      }
    },
  },
  mounted() {
    // show example for Simple Diff
    this.showDiffExample();
    this.getPacket();
  },
};
</script>

<style></style>

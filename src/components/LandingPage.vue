<template>
  <div>
    <v-container>
      <v-card elevation="8">
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
              @click="cleanHex">
            Clean hex
          </v-btn>
          <v-btn color="primary" @click="goToHex" large>Decode</v-btn>
          <v-btn text @click="reset">Reset</v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="showExamples">Next Example</v-btn>
        </v-card-actions>
      </v-card>
      <v-card style="margin-top: 2rem" v-if="decode">
        <div v-if="loading">
          <v-card-title>Loading packet...</v-card-title>
          <v-card-subtitle>Loading</v-card-subtitle>
          <v-card-text class="text-center">
            <v-progress-circular
                indeterminate
                color="primary"
            ></v-progress-circular>
          </v-card-text>
        </div>
        <div v-else-if="structure.length > 0">
          <v-card-title>Packet summary</v-card-title>
          <v-card-subtitle>{{ this.header.join(" / ") }}</v-card-subtitle>
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
        </div>
        <div v-else>

        </div>
        <v-alert
            v-if="alert"
            v-model="alert"
            border="left"
            type="error"
            close-text="Close Alert"
            dark
            dismissible
        >
          Error: Can not properly decode the hex.
        </v-alert>
      </v-card>
      <v-card id="space" v-if="structure" v-for="s in structure" :key="s.id">
        <v-card-title>{{ s.name }}</v-card-title>
        <v-card-subtitle>{{ s.tshark_name }}</v-card-subtitle>
        <v-card-text>
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title>{{ s.length }}{{ s.length_unit }}</v-list-item-title>
              <v-list-item-subtitle>Packet Length</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title>
                <pre><code>{{ s.repr }}</code></pre>
              </v-list-item-title>
              <v-list-item-subtitle>Scapy code representation</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-textarea
              id="hex"
              filled
              name="input-7-4"
              label="tshark raw summary"
              :value="s.tshark_raw_summary.join('\n')"
              auto-grow
              readonly
          ></v-textarea>

        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import MessageService from "../services/messageService.js";

export default {
  name: "LandingPage",
  data() {
    return {
      hexValue: "",
      decode: false,
      loading: false,
      structure: [],
      summary: [],
      header: [],
      alert: false
    }
  },
  methods: {
    goToHex() {
      this.hexValue = this.hexValue.replace(/\s/g, '');
      this.$router.replace(`/hex/${this.hexValue}`);
      this.loading = true
      this.showPacket();
      this.getPacket();
    },
    read() {
      if (this.$route.query["redirect"]) {
        this.hexValue = this.$route.query["redirect"];
        this.goToHex();
      } else {
        this.hexValue = this.$route.params.hex_string
      }
      this.showPacket();
    },
    reset() {
      this.hexValue = "";
      this.decode = false;
      this.alert = false;
      this.loading = false;
      this.resetData();
      this.$router.replace("/hex/")
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
      } catch (error) {
      }
    },
    async getPacket() {
      if (this.hexValue !== "undefined") {
        this.loading = true;
        this.alert = false;
        this.resetData();
        try {
          const hexResponse = await MessageService.getHex(this.hexValue);
          this.structure = hexResponse["structure"];
          this.summary = hexResponse["summary"];
          if (this.structure.length === 0) {
            throw "Empty Structure";
          }
        } catch (err) {
          this.loading = false;
          this.alert = true;
          return
        }
        this.loading = false;
        this.alert = false;
        this.packData();
      }
    },
    packData() {
      this.header = [];
      this.structure.forEach(packet => {
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
      let stack = []
      let regex = new RegExp("[0-9a-fA-F]{1,2}")
      value.forEach(h => {
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
        "ff ff ff ff ff ff 00 00 00 00 00 00 08 00 45 00 00 71 00 01 00 00 40 29 7c 61 7f 00 00 01 7f 00 00 01 60 00 00 00 00 35 2f 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 35 00 35 00 31 00 00 73 6f 6d 65 20 72 61 6e 64 6f 6d 20 73 74 72 69 6e 67 20 31 31 32 33 34 34 35 39 38 32 37 33 34 39 38 32 37 33 34 32 33 34"
      ];
      let r_value = Math.floor(Math.random() * example_array.length);
      this.hexValue = example_array[r_value];
    }
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
}
</script>

<style>
#hex {
  font-family: monospace, monospace;
}

#space {
  margin-top: 1rem;
}
</style>
<template>
  <div>
    <v-card style="text-align: center">
      <p>I want to create a/an...</p>
      <v-text-field
        label="Search"
        prepend-icon="mdi-magnify"
        v-model="filter"
      ></v-text-field>
      <v-virtual-scroll
        height="100"
        :item-height="50"
        :items="filtered_packets"
      >
        <template v-slot:default="{ item }">
          <v-chip
            v-for="(packet, index) in item"
            :key="index"
            style="margin-left: 10px; margin-top: 10px"
            @click="handleAdd"
            :class="{ blue: pickedPackets.includes(packet) }"
          >
            {{ packet }}
          </v-chip>
        </template>
      </v-virtual-scroll>
      <v-btn @click="get_packets" color="orange">CREATE</v-btn>
    </v-card>
    <v-card style="margin-top: 1rem" v-if="pickedPackets.length">
      <v-stepper v-model="stepper">
        <v-stepper-header
          ><v-stepper-step
            v-for="(protocol, index) in pickedPackets"
            :key="index"
            :step="index"
            @click="stepper = index"
            style="cursor: pointer"
          >
            {{ protocol }}
          </v-stepper-step>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content
            v-for="(input, protocolId) in inputs"
            :key="protocolId"
            :step="protocolId"
          >
            <v-form>
              <v-container>
                <v-row>
                  <v-col cols="12" class="flex">
                    <v-text-field
                      v-for="(text, index) in input"
                      :key="index"
                      :label="text"
                      :value="res[protocolId][pickedPackets[protocolId]][text]"
                      v-model="res[protocolId][pickedPackets[protocolId]][text]"
                      class="textInput"
                      width="30px"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
            <v-btn @click="stepper--" v-if="stepper > 0">Previous</v-btn>
            <v-btn
              style="float: right"
              @click="stepper++"
              v-if="stepper < inputs.length - 1"
              >Next</v-btn
            >
            <v-btn style="float: right" v-else @click="handleCreate"
              >Create packet</v-btn
            >
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-card>
    <v-card
      style="padding: 10px; margin-top: 1rem"
      elevation="6"
      v-if="createdHex"
    >
      <v-card-title>Your packet</v-card-title>
      <v-textarea
        name="input-7-4"
        solo
        auto-grow
        readonly
        :value="createdHex"
        label="Hexdump"
        elevation="6"
      ></v-textarea>
      <v-btn class="button" color="blue">Copy</v-btn>
      <v-btn v-if="upperCase" color="indigo" @click="changeCasing"
        >To lower case</v-btn
      >
      <v-btn v-else color="indigo" @click="changeCasing">To upper case</v-btn>
      <v-btn v-if="spacing" color="orange" @click="changeSpacing"
        >Remove spacing</v-btn
      >
      <v-btn v-else color="orange" @click="changeSpacing">Add spacing</v-btn>
    </v-card>
  </div>
</template>

<script>
import ApiService from "../services/apiService.js";
export default {
  data() {
    return {
      packets: [["TCP", "IP", "DNS", "UDP", "GRE", "IPv6", "PPTP", "Ether"]],
      packet: null,
      pickedPackets: [],
      res: null,
      inputs: [],
      stepper: null,
      filter: "",
      createdHex: null,
      upperCase: false,
      spacing: true,
    };
  },
  computed: {
    filtered_packets() {
      return [
        this.packets[0].filter((x) =>
          x.toLowerCase().includes(this.filter.toLowerCase())
        ),
      ];
    },
  },
  methods: {
    async get_packets() {
      this.createdHex = null;
      this.res = await ApiService.getScapy(this.pickedPackets);
      this.inputs = [];
      for (let i = 0; i < this.res.length; i++) {
        let temp_packet = Object.keys(this.res[i]);
        console.log(temp_packet);
        this.inputs.push(Object.keys(this.res[i][temp_packet]));
      }
      console.log(this.res[0][Object.keys(this.res[0])]);
      this.stepper = -1;
      /*
      this.steps = [...Array(this.inputs.length).keys()].filter(
        (n) => !(n % 3)
      );
      */
    },
    async handleCreate() {
      this.res.forEach((element) => {
        let temp_packet = Object.keys(element);
        Object.keys(element[temp_packet]).forEach((header) => {
          if (/^-?\d+$/.test(element[temp_packet][header])) {
            element[temp_packet][header] = Number(element[temp_packet][header]);
          }
        });
      });
      const newPacket = await ApiService.createPacket(this.res);
      this.createdHex = newPacket["hex"];
      console.log(this.createdHex);
    },
    handleAdd(el) {
      const protocol = el.srcElement.innerText;
      if (!this.pickedPackets.includes(protocol)) {
        this.pickedPackets.push(protocol);
      } else {
        this.pickedPackets.splice(this.pickedPackets.indexOf(protocol), 1);
      }
    },
    changeCasing() {
      if (this.upperCase) {
        this.createdHex = this.createdHex.toLowerCase();
        this.upperCase = false;
      } else {
        this.createdHex = this.createdHex.toUpperCase();
        this.upperCase = true;
      }
    },
    changeSpacing() {
      this.createdHex = this.createdHex.replace(/\s+/g, "");
      if (this.spacing) {
        this.spacing = false;
      } else {
        for (let i = 0; i < this.createdHex.length; i += 3) {
          this.createdHex =
            this.createdHex.slice(0, i) + " " + this.createdHex.slice(i);
        }
        this.spacing = true;
      }
    },
  },
};
</script>

<style>
.scroll-wrapper {
  display: flex;
  flex-direction: row;
  text-align: left;
}
.flex {
  display: flex;
  flex-wrap: wrap;
}
.textInput {
  margin: 10px;
}
.button {
  float: right;
}
</style>
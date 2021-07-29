<template>
  <div>
    <v-card style="padding: 10px; margin-top: 1rem" elevation="6">
      <v-card-title>Your Packet</v-card-title>
      <v-textarea
        name="input-7-4"
        solo
        auto-grow
        readonly
        :value="createdHex"
        label="Hexdump"
        elevation="6"
      ></v-textarea>
      <div class="actionButtons">
        <v-btn @click="createdHex = null" color="red" class="white--text"
          ><v-icon>mdi-cancel</v-icon>Clear</v-btn
        >
        <v-btn class="button white--text" color="blue" @click="copy"
          ><v-icon>mdi-content-copy</v-icon>Copy</v-btn
        >
        <v-btn
          v-if="upperCase"
          color="indigo"
          @click="changeCasing"
          class="white--text actionButton"
          ><v-icon>mdi-arrow-down</v-icon>To lower case</v-btn
        >
        <v-btn
          v-else
          color="indigo"
          @click="changeCasing"
          class="white--text actionButton"
          ><v-icon>mdi-arrow-up</v-icon>To upper case</v-btn
        >
        <v-btn
          v-if="spacing"
          color="orange"
          @click="changeSpacing"
          class="white--text actionButton"
          ><v-icon>mdi-window-close</v-icon>Remove spacing</v-btn
        >
        <v-btn
          v-else
          color="orange"
          @click="changeSpacing"
          class="white--text actionButton"
          ><v-icon>mdi-plus</v-icon>Add spacing</v-btn
        >
      </div>
    </v-card>

    <v-card style="margin-top: 10px">
      <v-stepper v-model="stepper" height="">
        <v-stepper-header>
          <v-stepper-step step="0" @click="stepper = 0" style="cursor: pointer">
            Choose packets
          </v-stepper-step>
          <div v-for="(protocol, index) in displayPackets" :key="index">
            <v-stepper-step
              :step="index + 1"
              @click="stepper = index + 1"
              style="cursor: pointer"
            >
              {{ protocol }}
            </v-stepper-step>
          </div>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content step="0">
            <div class="topBar">
              <p style="padding-right: 5px">I want to create a/an...</p>
              <div style="display: flex">
                <div
                  v-for="(pickedPacket, index) in pickedPackets"
                  :key="index"
                  style="display: flex"
                >
                  <b style="cursor: pointer">
                    <v-icon x-small>mdi-window-close</v-icon>
                    <span @click="handleAdd" style="margin-left: 3px">{{
                      pickedPacket
                    }}</span>
                  </b>
                  <div
                    v-if="index != pickedPackets.length - 1"
                    style="margin: 0 5px 0 5px"
                  >
                    /
                  </div>
                </div>
              </div>
              <v-btn
                style="margin-left: auto"
                @click="get_packets"
                color="orange"
                class="white--text"
                :disabled="!pickedPackets.length"
                >Next <v-icon>mdi-arrow-right</v-icon></v-btn
              >
            </div>
            <div class="searchInput">
              <v-text-field
                label="Search"
                prepend-icon="mdi-magnify"
                v-model="filter"
              ></v-text-field>
              <v-icon
                style="position: absolute; right: 1.3rem; top: 5.5rem"
                dense
                @click="filter = ''"
                >mdi-window-close</v-icon
              >
            </div>
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
                  :class="{ blue: pickedPackets.includes(packet.name) }"
                >
                  {{ packet.name }}
                </v-chip>
              </template>
            </v-virtual-scroll>
          </v-stepper-content>
          <v-stepper-content
            v-for="(input, protocolId) in inputs"
            :key="protocolId"
            :step="protocolId + 1"
          >
            <v-btn
              @click="stepper--"
              v-if="stepper > 0"
              color="orange"
              class="white--text"
              ><v-icon>mdi-arrow-left</v-icon>Back
            </v-btn>
            <v-btn
              style="float: right"
              @click="stepper++"
              v-if="stepper < inputs.length"
              color="orange"
              class="white--text"
              >Next <v-icon>mdi-arrow-right</v-icon></v-btn
            >
            <v-btn
              v-else
              style="float: right"
              @click="handleCreate"
              color="green"
              class="white--text"
              >Create packet<v-icon>mdi-package-variant-closed</v-icon></v-btn
            >
            <v-form>
              <v-container>
                <v-row>
                  <v-col cols="12" class="flex">
                    <v-text-field
                      v-for="(text, index) in input"
                      :key="index"
                      :label="text"
                      :value="
                        res[protocolId][
                          packets[
                            packets.findIndex(
                              (x) => x.name === displayPackets[protocolId]
                            )
                          ].scapy_name
                        ][text]
                      "
                      v-model="
                        res[protocolId][
                          packets[
                            packets.findIndex(
                              (x) => x.name === displayPackets[protocolId]
                            )
                          ].scapy_name
                        ][text]
                      "
                      class="textInput"
                      width="30px"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-stepper-content>
        </v-stepper-items>
        <v-tooltip right>
          <template v-slot:activator="{ on, attrs }">
            <v-icon v-bind="attrs" v-on="on"> mdi-information </v-icon>
          </template>
          <span>
            <ul>
              <li>You can select up to 4 protocols</li>
              <li>Headers with default value can't be empty</li>
              <li>Options should be separated with a comma</li>
              <li>TCP breaks when options are provided</li>
            </ul>
          </span>
        </v-tooltip>
      </v-stepper>
    </v-card>
    <Toast type="success" :trigger="successSw" :key="0"
      ><template #info> Hex has been copied </template></Toast
    >
    <Toast type="warning" :trigger="alertSw" :key="1"
      ><template #info> Hex is empty </template></Toast
    >
    <Toast type="error" :trigger="errorSw" :key="2"
      ><template #info> Error </template></Toast
    >
  </div>
</template>

<script>
import ApiService from "../services/apiService.js";
import Toast from "./Toast.vue";

export default {
  components: { Toast },
  data() {
    return {
      // Some protocols have different function name
      // and "to_list" key (ex. Ethernet) so they
      // have to be handled in core to be able to add them here
      packets: [
        { name: "Ether", scapy_name: "Ethernet" },
        { name: "IP", scapy_name: "IP" },
        { name: "UDP", scapy_name: "UDP" },
        { name: "TCP", scapy_name: "TCP" },
        { name: "DNS", scapy_name: "DNS" },
        { name: "GRE", scapy_name: "GRE" },
        { name: "IPv6", scapy_name: "IPv6" },
        { name: "PPTP", scapy_name: "PPTP" },
        { name: "DHCP", scapy_name: "DHCP options" },
        { name: "ICMP", scapy_name: "ICMP" },
        { name: "Raw", scapy_name: "Raw" },
        { name: "ARP", scapy_name: "ARP" },
        { name: "VXLAN", scapy_name: "VXLAN" },
        { name: "Padding", scapy_name: "Padding" },
        { name: "PadN", scapy_name: "PadN" },
        { name: "Pad1", scapy_name: "Pad1" },
        { name: "MGCP", scapy_name: "MGCP" },
        { name: "Loopback", scapy_name: "Loopback" },
        { name: "LLTD", scapy_name: "LLTD" },
        { name: "LLC", scapy_name: "LLC" },
        { name: "ISAKMP", scapy_name: "ISAKMP" },
        { name: "HSRP", scapy_name: "HSRP" },
        { name: "ESP", scapy_name: "ESP" },
        { name: "EAP", scapy_name: "EAP" },
        { name: "EAPOL", scapy_name: "EAPOL" },
        { name: "BOOTP", scapy_name: "BOOTP" },
        { name: "AH", scapy_name: "AH" },
      ],
      packet: null,
      pickedPackets: [],
      displayPackets: [],
      res: null,
      inputs: [],
      stepper: 0,
      filter: "",
      createdHex: null,
      upperCase: false,
      spacing: true,
      successSw: 0,
      alertSw: 0,
      errorSw: 0,
    };
  },
  computed: {
    filtered_packets() {
      // Returns packets that match the filter
      return [
        this.packets.filter((x) =>
          x.name.toLowerCase().includes(this.filter.toLowerCase())
        ),
      ];
    },
  },
  methods: {
    delay(seconds) {
      return new Promise((res) => setTimeout(res, seconds * 1000));
    },
    async get_packets() {
      try {
        this.res = await ApiService.getScapy(this.pickedPackets);
        if (!this.res.length) throw "Empty structure";
      } catch (err) {
        this.errorSw = !this.errorSw;
        return;
      }
      this.displayPackets = [];
      this.inputs = [];
      for (let i = 0; i < this.res.length; i++) {
        let temp_packet = Object.keys(this.res[i]);
        this.inputs.push(Object.keys(this.res[i][temp_packet]));
      }
      this.displayPackets = this.pickedPackets.slice();
      await this.delay(0.5);
      this.stepper++;
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
          if (
            header === "options" &&
            element[temp_packet][header].includes(",")
          ) {
            element[temp_packet][header] = element[temp_packet][header]
              .trim()
              .split(",");
          }
        });
      });
      let newPacket = "";
      try {
        newPacket = await ApiService.createPacket(this.res);
      } catch {
        this.errorSw = !this.errorSw;
        return;
      }
      this.createdHex = newPacket["hex"];
      console.log(this.createdHex);
    },
    handleAdd(el) {
      const protocol = el.srcElement.innerText;
      if (
        !this.pickedPackets.includes(protocol) &&
        this.pickedPackets.length < 4
      ) {
        this.pickedPackets.push(protocol);
      } else if (this.pickedPackets.includes(protocol)) {
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
    async copy() {
      if (this.createdHex) {
        await navigator.clipboard.writeText(this.createdHex);
        this.successSw = !this.successSw;
      } else this.alertSw = !this.alertSw;
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
.topBar {
  display: flex;
}
.actionButton {
  margin-left: 3px;
}
.searchInput {
  display: flex;
}
</style>
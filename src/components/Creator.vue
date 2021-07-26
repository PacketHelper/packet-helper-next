<template>
  <div>
    <v-card style="text-align: center">
      <p>I want to create a/an...</p>
      <v-select v-model="packet" :items="packets" label="Packet"></v-select>
      <v-virtual-scroll height="100" :item-height="50" :items="packets">
        <template v-slot:default="{ item }">
          <v-btn
            depressed
            v-for="(packet, index) in item"
            :key="index"
            style="margin-left: 10px; margin-top: 10px"
            @click="handleAdd"
          >
            {{ packet }}
          </v-btn>
        </template>
      </v-virtual-scroll>
      <v-btn @click="get_packets" color="orange">CREATE</v-btn>
    </v-card>
    <v-card v-if="inputs">
      <v-form>
        <v-container>
          <v-row v-for="step in steps" :key="step">
            <v-col>
              <v-text-field
                v-if="inputs[step]"
                :label="inputs[step]"
                :value="res[packet][inputs[step]]"
                v-model="res[packet][inputs[step]]"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-if="inputs[step + 1]"
                :label="inputs[step + 1]"
                :value="res[packet][inputs[step + 1]]"
                v-model="res[packet][inputs[step + 1]]"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-if="inputs[step + 2]"
                :label="inputs[step + 2]"
                :value="res[packet][inputs[step + 2]]"
                v-model="res[packet][inputs[step + 2]]"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
      <v-btn @click="handleCreate">Create packet</v-btn>
    </v-card>
  </div>
</template>

<script>
import ApiService from "../services/apiService.js";
export default {
  data() {
    return {
      packets: [["TCP", "IP", "DNS", "UDP"]],
      packet: null,
      res: null,
      inputs: null,
      steps: null,
    };
  },
  methods: {
    async get_packets() {
      this.res = await ApiService.getScapy(this.packet);
      this.inputs = Object.keys(this.res[this.packet]);
      this.steps = [...Array(this.inputs.length).keys()].filter(
        (n) => !(n % 3)
      );
    },
    handleCreate() {
      console.log(this.res);
    },
    handleAdd(el) {
      console.log(el.srcElement.innerText);
    },
  },
};
</script>

<style>
.scroll-wrapper {
  display: flex;
  flex-direction: row;
}
</style>
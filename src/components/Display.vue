<template>
  <div class="wrapper">
    <v-expansion-panel style="margin-top: 0.15rem" elevation="8" rounded>
      <v-expansion-panel-header>
        <div>
          <ul>
            <li>
              <v-card-title> {{ data.name }} </v-card-title>
              <v-card-subtitle> {{ data.tshark_name }} </v-card-subtitle>
            </li>
          </ul>
        </div>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-card-text>
          <ul>
            <li>Packet length: {{ data.length }}{{ data.length_unit }}</li>
            <DropDown>
              <template v-slot:title>
                <b>
                <li class="collapse">
                  Scapy code representation:
                </li>
                <i class="fa-li fa fa-caret-right"></i></b>
              </template>
              <template v-slot:content>
                <ul>
                  <li>
                    <code>{{ data.repr }}</code>
                  </li>
                </ul>
              </template>
            </DropDown>
            <div v-if="sortedData">
              <div
                class="raw-data"
                v-for="(tshark, key) in sortedData"
                :key="key"
              >
                <div v-if="tshark.children">
                  <DropDown>
                    <template v-slot:title>
                      <b>
                      <li class="collapse">
                        {{ tshark.name }}: {{ tshark.value }}
                      </li>
                      <i class="fa-li fa fa-caret-right"></i></b>
                    </template>
                    <template v-slot:content>
                      <ul>
                        <div v-for="(child, key) in tshark.children" :key="key">
                          <div v-if="child.children">
                            <DropDown>
                              <template v-slot:title>
                                <b>
                                <li class="collapse">
                                  {{ child.name }}: {{ child.value }}
                                </li>
                                <i class="fa-li fa fa-caret-right"></i>
                                </b>
                              </template>
                              <template v-slot:content>
                                <ul>
                                  <li
                                    v-for="(nestedChild, key) in child.children"
                                    :key="key"
                                  >
                                    <code
                                      >{{ nestedChild.name }}:
                                      {{ nestedChild.value }}</code
                                    >
                                  </li>
                                </ul>
                              </template>
                            </DropDown>
                          </div>
                          <div v-else>
                            <li>
                              <code>{{ child.name }}: {{ child.value }} </code>
                            </li>
                          </div>
                        </div>
                      </ul>
                    </template>
                  </DropDown>
                </div>
                <div v-else-if="tshark.value">
                  <li><code>{{ tshark.name }}: {{ tshark.value }}</code></li>
                </div>
              </div>
            </div>
            <div v-else-if="!supported">
              <li v-for="(tshark, key) in data.tshark_raw_summary" :key="key">
                <code>{{ tshark }}</code>
              </li>
            </div>
            <div v-else>
              <h3>An unknown error has occured</h3>
            </div>
          </ul>
        </v-card-text>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import DropDown from "./DropDown.vue";
import Protocols from "../services/protocols.js";

export default {
  props: ["data"],
  components: { DropDown },
  data() {
    return {
      items: [],
      sortedData: null,
      supported: true,
    };
  },
  // Handle the way data is displayed
  mounted() {
    // When protocol is not supported, don't do anything
    if (!Protocols[this.data.tshark_name.toUpperCase()]) {
      this.supported = false
      this.$emit("warning");
      return;
    }

    let copy = this.data.tshark_raw_summary.slice();
    //console.log(this.data.tshark_raw_summary)
    let bits = [];
    let names = [];

    // Prepare arrays for bits and DNS nameservers
    copy.forEach((element) => {
      if (element.includes(" =")) {
        bits.push({
          name: element.substring(0, element.indexOf(":")),
          value: element.substring(element.indexOf(":") + 1),
        });
      }
      // looks for keys that has dots and there are less than 4 of them
      // ex.: www.youtube.com
      else if (
        element.substring(0, element.indexOf(":")).split(".").length - 1 &&
        element.substring(0, element.indexOf(":")).split(".").length - 1 < 4
      ) {
        names.push({
          name: element.substring(0, element.indexOf(":")),
          value: element.substring(element.indexOf(":") + 1),
        });
      }
    });

    // Executes function that coresponds to tshark's name
    let ord = Protocols[this.data.tshark_name.toUpperCase()](bits, 4, names);

    // Insert values into final object
    ord.forEach((element) => {
      let re_parent = new RegExp("^" + element.name);
      let index_parent = copy.findIndex((el) => re_parent.test(el));
      if (index_parent !== -1) {
        element.value = copy[index_parent]
          .substring(copy[index_parent].indexOf(":") + 1)
          .trim();
        // Remove processed item to avoid duplicates
        copy.splice(index_parent, 1);
      }

      if (element.children)
        element.children.forEach((child) => {
          let re_child = new RegExp("^" + child.name + ":");
          let index_child = copy.findIndex((el) => re_child.test(el));
          if (index_child !== -1) {
            child.value = copy[index_child]
              .substring(copy[index_child].indexOf(":") + 1)
              .trim();
            copy.splice(index_child, 1);
          }

          if (child.children) {
            child.children.forEach((nested_child) => {
              let re_nested_child = new RegExp("^" + nested_child.name + ":");
              let index_nested_child = copy.findIndex((el) =>
                re_nested_child.test(el)
              );
              if (index_nested_child !== -1) {
                nested_child.value = copy[index_nested_child]
                  .substring(copy[index_nested_child].indexOf(":") + 1)
                  .trim();
                copy.splice(index_nested_child, 1);
              }
            });
          }
        });
    });

    // Finally display the data
    this.sortedData = ord;
  },
};
</script>

<style>
</style>
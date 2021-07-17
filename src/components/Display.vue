<template>
  <div class="wrapper">
    <v-expansion-panel style="margin-top: 1rem" elevation="8" rounded>
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
                  <li class="collapse">Scapy code representation:</li>
                  <i class="fa-li fa fa-caret-right"></i
                  ></b>
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
                        <i class="fa-li fa fa-caret-right"></i
                      ></b>
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
                  <li>
                    <code>{{ tshark.name }}: {{ tshark.value }}</code>
                  </li>
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
  components: {DropDown},
  data() {
    return {
      items: [],
      sortedData: null,
      supported: true,
    };
  },
  // Handle the way data is displayed
  mounted() {
    // When protocol is not supported, emits a warning
    // and returns
    if (!Protocols[this.data.tshark_name.toUpperCase()]) {
      this.supported = false;
      this.$emit("warning");
      return;
    }

    let copy = this.data.tshark_raw_summary.slice();
    let bits = [];
    let names = [];
    let options = [];
    let length = 0;

    // Prepare arrays for bits, DNS nameservers, TCP Options
    // and TELNET data
    copy.forEach((element) => {
      let name = element.substring(0, element.indexOf(":"));
      let value = element.substring(element.indexOf(":") + 1);
      if (element.includes(" =")) {
        bits.push({
          name: name,
          value: value,
        });
      }
          // looks for keys that has dots and there are less than 4 of them
      // ex.: www.youtube.com, github.com, www.my.example.com
      else if (name.split(".").length - 1 && name.split(".").length - 1 < 4) {
        names.push({
          name: name,
          value: value,
        });
      } else if (element.includes("TCP Option")) {
        if (element.includes(":")) options.push(name);
        else options.push(element);
      }
      // For TELNET protocol
      else if (element.includes("Data")) length++;
    });

    // Executes function that coresponds to tshark's name
    let ord = Protocols[this.data.tshark_name.toUpperCase()](
        bits,
        length,
        names,
        options
    );

    // Insert values into ord
    ord.forEach((element) => {
      let re_parent = new RegExp("^" + element.name);
      let index_parent = copy.findIndex((el) => re_parent.test(el));

      if (index_parent !== -1) {
        if (copy[index_parent].includes(":")) {
          // Some keys are semi-static and have to be handled with regex
          element.name = copy[index_parent]
              .substring(0, copy[index_parent].indexOf(":"))
              .trim();
          element.value = copy[index_parent]
              .substring(copy[index_parent].indexOf(":") + 1)
              .trim();
        } else {
          element.value = copy[index_parent]
              .substring(
                  copy[index_parent].indexOf("(") + 1,
                  copy[index_parent].indexOf(")")
              )
              .trim();
        }
        // Some headers have the same value as its key
        if (element.value === element.name) element.value = "";

        // Remove processed item to avoid duplicates
        copy.splice(index_parent, 1);
      }

      // Everything up to the end of foreach
      // is being handled in the same way as
      // parent element
      if (element.children)
        element.children.forEach((child) => {
          let re_child = new RegExp("^" + child.name + ":");
          let index_child = copy.findIndex((el) => re_child.test(el));

          if (index_child !== -1) {
            child.name = copy[index_child]
                .substring(0, copy[index_child].indexOf(":"))
                .trim();
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
                nested_child.name = copy[index_nested_child]
                    .substring(0, copy[index_nested_child].indexOf(":"))
                    .trim();
                nested_child.value = copy[index_nested_child]
                    .substring(copy[index_nested_child].indexOf(":") + 1)
                    .trim();
                copy.splice(index_nested_child, 1);
              }
            });
          }
        });
    });

    // Removes headers with no values
    // It was the last feature I added and didn't test it very much
    // so if something breaks its probably because of this
    let final = [];
    for (let i = 0; i < ord.length; i++) {
      let children = [];
      let nested_children = [];
      let temp = null;

      if (ord[i].children) {
        for (let j = 0; j < ord[i].children.length; j++) {
          if (ord[i].children[j].children) {
            for (let k = 0; k < ord[i].children[j].children.length; k++) {
              if (ord[i].children[j].children[k].value) {
                nested_children.push(ord[i].children[j].children[k]);
              }
            }
          }
          if (nested_children.length || ord[i].children[j].value) {
            temp = ord[i].children[j];
            temp.children =
                nested_children.length === 0 ? null : nested_children;
            children.push(temp);
          }
        }
      }
      if (children.length || ord[i].value) {
        temp = ord[i];
        temp.children = children.length === 0 ? null : children;
        final.push(temp);
      }
    }

    // Finally display the data
    this.sortedData = final;
  },
};
</script>

<style>
</style>
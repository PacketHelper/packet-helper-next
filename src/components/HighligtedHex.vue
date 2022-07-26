<template>
  <div class="wrapper">
    <div v-html="highlight()"></div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class HighligtedHex extends Vue {
  @Prop() entireHex: string | undefined;
  @Prop() partlyHex: string | undefined;

  highlight(): string {
    const NOT_FOUND = "Not found";
    if (this.entireHex === undefined || this.partlyHex === undefined) {
      return NOT_FOUND;
    }

    const entire = this.entireHex.replace(/\s/g, "").toUpperCase();
    const part = this.partlyHex.replace(/\s/g, "").toUpperCase();
    const matchStartingPoint = entire.indexOf(part);
    if (matchStartingPoint === -1) {
      return NOT_FOUND;
    }

    const startCell = matchStartingPoint / 2;
    const endCell = startCell + part.length / 2 - 1;

    let separatedHex = this.split(entire);
    if (separatedHex === null) {
      return NOT_FOUND;
    }

    separatedHex[
      startCell
    ] = `<span class="highlightText">${separatedHex[startCell]}`;
    separatedHex[endCell] = `${separatedHex[endCell]}</span>`;

    if (!this.partlyHex) {
      return this.entireHex;
    }

    for (let i = 1; i <= separatedHex?.length; ++i) {
      if (i % 16 === 0) {
        separatedHex[i - 1] = `${separatedHex[i - 1]}<br />`;
      }
    }
    return separatedHex.join(" ");
  }

  split(splitted: string): RegExpMatchArray | null {
    if (splitted === undefined) {
      return null;
    }

    return splitted.match(/.{1,2}/g);
  }
}
</script>

<style>
.highlightText {
  background: rgb(255, 255, 0);
}
</style>

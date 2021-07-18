<template>
  <div class="wrapper">
    <div class="dropdown-title" @click="HandleClick">
      <slot name="title"></slot>
    </div>

    <v-expand-transition appear>
      <div class="dropdown-item" v-if="toggle">
        <slot name="content"></slot>
      </div>
    </v-expand-transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      toggle: false,
    };
  },
  methods: {
    HandleClick(el) {
      this.toggle = !this.toggle;

      // Pretty bad way to do this imo but
      // couldn't come up with anything better
      if (el.srcElement.className === "collapse") {
        if (this.toggle)
          el.srcElement.nextElementSibling.className = "fa-li fa fa-caret-down";
        else
          el.srcElement.nextElementSibling.className =
            "fa-li fa fa-caret-right";
      } else {
        if (this.toggle) el.srcElement.className = "fa-li fa fa-caret-down";
        else el.srcElement.className = "fa-li fa fa-caret-right";
      }
    },
  },
};
</script>

<style>
.dropdown-title {
  cursor: pointer;
}
.dropdown-item {
  max-height: 2000px;
}
.v-expansion-panel {
  font-family: "Gidole";
}
.dropdown-title {
  cursor: pointer;
}

i {
  margin-left: 6px;
}
</style>
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

.drop-enter-active {
  overflow: hidden;
  animation: drop-enter 0.8s ease;
}
.drop-leave-to {
  opacity: 0;
  max-height: 0;
}
.drop-leave-active {
  overflow: hidden;
  transition: all 0.3s ease;
}

@keyframes drop-enter {
  0% {
    opacity: 0;
    max-height: 0;
  }
  100% {
    opacity: 1;
  }
}
.collapse {
  list-style-type: none;
}

.v-expansion-panel {
  font-family: monospace, monospace;
}

.dropdown-title {
  cursor: pointer;
}

.rotate {
  list-style-type: none;
}

i {
  margin-left: 6px;
}
</style>

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

      // Switches list styles
      if (this.toggle) el.explicitOriginalTarget.className = "expand";
      else el.explicitOriginalTarget.className = "collapse";
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
/*
.drop-enter {
  opacity: 0;
  max-height: 0;
}
*/
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
  position: relative;
  left: -0.7rem;
}
.collapse::before {
  font-family: "Font Awesome 5 Free";
  content: "\f0da";
}
.expand {
  list-style-type: none;
  position: relative;
  left: -0.91rem;
}
.expand::before {
  font-family: "Font Awesome 5 Free";
  content: "\f0dd";
}
.v-expansion-panel {
  font-family: monospace, monospace;
}
.dropdown-title {
  cursor: pointer;
}

i {
  margin-left: 6px;
}
</style>
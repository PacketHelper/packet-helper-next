<template>
  <div class="wrapper">
    <div class="dropdown-title" @click="HandleClick">
      <slot name="title"></slot>
    </div>

    <transition name="drop" active>
      <div class="dropdown-item" v-if="toggle">
        <slot name="content"></slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      toggle: false
    }
  },
  methods: {
    HandleClick() {
      this.toggle = !this.toggle
    }
  },
}
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
  0% {opacity: 0; max-height: 0}
  100% {opacity: 1}
}
</style>
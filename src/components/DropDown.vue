<template>
  <div class="wrapper">
    <div class="dropdown-title" @click="HandleClick">
      <slot name="title"></slot>
    </div>

    <transition name="drop" appear>
      <div class="dropdown-item" v-if="toggle">
        <slot name="content"></slot>
      </div>
    </transition>
  </div>
</template>

<script>
import gsap from "gsap";

export default {
  data() {
    return {
      toggle: false,
    };
  },
  methods: {
    HandleClick(el) {
      this.toggle = !this.toggle;
      console.log(el.explicitOriginalTarget);
      if (this.toggle) el.explicitOriginalTarget.className += " rotate";
      else
        el.explicitOriginalTarget.className =
          el.explicitOriginalTarget.className
            .substring(
              0,
              el.explicitOriginalTarget.className.indexOf(" rotate")
            )
            .trim();
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
  list-style-type: georgian;
}
/*
.collapse::before {
  content: "\2192";
  margin-left: -15px;
}
*/
.dropdown-item {
  font-family: "Gidole";
}
.dropdown-title {
  cursor: pointer;
}

.rotate {
  list-style-type: disc;
}
/*
.rotate::before {
  content: "\2193";
  margin-left: -15px;
}
*/
</style>
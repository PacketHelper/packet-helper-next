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
            toggle: false,
            items: []
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
    max-height: 500px;
}
.drop-enter {
    opacity: 0;
    max-height: 0;
}
.drop-enter-active {
    transition: all 1s ease;
}
.drop-leave-to {
    opacity: 0;
    max-height: 0;
}
.drop-leave-active {
    overflow: hidden;
    transition: all 0.4s ease;
}
@keyframes drop {
    0% { opacity: 0; max-height: 0px }
    100% { opacity: 1; max-height: 500px }
}
</style>
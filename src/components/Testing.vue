<template>
    <DropDown :data="random"></DropDown>
</template>

<script>
import DropDown from "./DropDown.vue"

export default {
    components: { DropDown },
    data() {
        return {
            random: "test"
        }
    }
}
</script>

<style>

</style>
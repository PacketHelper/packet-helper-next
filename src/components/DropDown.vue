<template>
    <div class="wrapper">
        <div v-if="data">
            <div class="dropdown-title" @click="HandleClick">
                <slot name="title"></slot>
            </div>

            <div class="item" v-if="toggle">
                <ul>
                    <li>Packet length: {{ data.length }}{{ data.length_unit }}</li>
                    <li>Scapy code representation: <code>{{ data.repr }}</code></li>
                    <div class="raw-data" v-for="(tshark, key) in items" :key="key">
                    <li>{{ tshark.name }}: {{ tshark.value }}</li>
                        <!--<div v-if="tshark.children.length">
                            <ul>
                                <li v-for="(child, key) in tshark.children" :key="key">
                                    {{ child }}
                                </li>
                            </ul>
                        </div>-->
                    </div>
                </ul>
            </div>
        </div>
        <div v-else>
            There was an error while loading data
        </div>
    </div>
</template>

<script>
export default {
    props: ['data'],
    data() {
        return {
            toggle: false,
            items: []
        }
    },
    methods: {
        HandleClick() {
            this.toggle = !this.toggle
            console.log("click")
        }
    },
    mounted() {
        //console.log(this.data.tshark_raw_summary)
        this.data.tshark_raw_summary.forEach(element => {
            // Submenu heuristics
            if(this.items.length) {
                if(
                    //element.includes("=") ||
                    // element.includes("Address") ||
                    // element.includes("Name") ||
                    // element.includes("Label") ||
                    // element.includes("Type") ||
                    // element.includes("Time to live") ||
                    // element.includes("Class") ||
                    // element.includes("CNAME") ||
                    // element.includes("length") ||
                    // element.includes("class") ||
                    // element.includes("Time since") ||
                    //element.includes("Bytes")
                    element.includes("klasdjlkfjdlfaj;lfkdajfkl;")
                    ) this.items[this.items.length - 1].children.push(element)
            }
            else {
                let obj = {}
                obj.name = element.substring(0, element.indexOf(":"))
                obj.value = element.substring(element.indexOf(":") + 1)
                obj.children = []
                this.items.push(obj)
            }
            console.log(this.items)  
        });
    }
}
</script>

<style>
.dropdown-title {
    cursor: pointer;
}
</style>
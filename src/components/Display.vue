<template>
    <div class="wrapper">
        <div v-if="data">
            <DropDown>
                <template v-slot:title>
                    <v-card>
                        <v-card-title>{{ data.name }}</v-card-title>
                        <v-card-subtitle>{{ data.tshark_name }}</v-card-subtitle>
                    </v-card>
                </template>

                <template v-slot:content>
                    <ul>
                        <li>Packet length: {{ data.length }}{{ data.length_unit }}</li>
                        <DropDown>
                            <template v-slot:title>
                                <li>Scapy code representation:</li>
                            </template>

                            <template v-slot:content>
                                <ul>
                                    <li> <code>{{ data.repr }}</code></li>
                                </ul>
                            </template>
                        </DropDown>
                        <div class="raw-data" v-for="(tshark, key) in items" :key="key">
                            <div v-if="tshark.children.length">
                                <DropDown>
                                    <template v-slot:title>
                                        <li>{{ tshark.name }}: {{ tshark.value }}</li>
                                    </template>

                                    <template v-slot:content v-if="tshark.children.length">
                                        <ul>
                                            <li v-for="(child, key) in tshark.children" :key="key">
                                                <code>{{ child }}</code>
                                            </li>
                                        </ul>
                                    </template>
                                </DropDown>
                            </div>

                            <div v-else>
                                <li>{{ tshark.name }}: {{ tshark.value }}</li>
                            </div>
                        </div>
                    </ul>
                </template>
            </DropDown>
        </div>

        <div v-else>
            There was an error while loading data
        </div>
    </div>
</template>

<script>
import DropDown from './DropDown.vue'

export default {
    props: ['data'],
    components: { DropDown },
    data() {
        return {
            items: []
        }
    },
    mounted() {
        //console.log(this.data.tshark_raw_summary)
        this.data.tshark_raw_summary.forEach(element => {
            // Submenu heuristics
            if(
                element.includes("=") ||
                element.includes("Address") ||
                //element.includes("Name") ||
                element.includes("Label") ||
                element.includes("Type") ||
                element.includes("Time to live") ||
                element.includes("Class") ||
                element.includes("CNAME") ||
                element.includes("length") ||
                element.includes("class") ||
                element.includes("Time since") ||
                element.includes("Bytes")
            ){
                if(this.items.length) {
                    this.items[this.items.length - 1].children.push(element)
                }
            }
            else {
                let obj = {}
                obj.name = element.substring(0, element.indexOf(":"))
                obj.value = element.substring(element.indexOf(":") + 1)
                obj.children = []
                console.log(obj)
                this.items.push(obj)
            }
            //console.log(this.items)  
        });
    }
}
</script>

<style>
.dropdown-title {
    cursor: pointer;
}
</style>
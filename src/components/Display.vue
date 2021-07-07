<template>
  <div class="wrapper">
    <div v-if="data">
      <v-card>
        <DropDown>
          <template v-slot:title>
            <v-card-title>{{ data.name }}</v-card-title>
            <v-card-subtitle>{{ data.tshark_name }}</v-card-subtitle>
          </template>

          <template v-slot:content>
            <code>
              <v-card-text>
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
                  <div class="raw-data" v-for="(tshark, key) in sortedData" :key="key">
                    <div v-if="tshark.children">
                      <DropDown>
                        <template v-slot:title>
                          <li class="collapse">{{ tshark.name }}: {{ tshark.value }}</li>
                        </template>

                        <template v-slot:content v-if="tshark.children">
                          <ul>
                            <li v-for="(child, key) in tshark.children" :key="key">
                              <code>{{ child.name }}: {{ child.value }}</code>
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
              </v-card-text>
            </code>
          </template>
        </DropDown>
      </v-card>
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
      items: [],
      sortedData: null
    }
  },
  methods: {
    ETH(bits) {
      let ord = [
        {name: 'Destination', children: [...bits.slice(0,2)]}, 
        {name: 'Source', children: [...bits.slice(2, 4)]}, // {name: 'Address', value: addresses[1]}
        {name: 'Type'}, 
        {name: 'Frame check sequence'}, 
        {name: 'FCS Status'}
      ]
      return ord
    },
    IP(bits) {
      let ord = [
        ...bits.slice(0, 1),
        {name: 'Differentiated Services Field', children: [
          ...bits.slice(2, 4)
        ]},
        {name: 'Total Length'},
        {name: 'Identification'},
        {name: 'Flags', children: [...bits.slice(4)]},
        {name: 'Time to live'},
        {name: 'Protocol'},
        {name: 'Header Checksum', children: [{name: 'Calculated Checksum'}]},
        {name: 'Header checksum status'}
      ]
      return ord
    },
    UDP() {
      //console.log(obj)
      let ord = [
        {name: 'Source Port'},
        {name: 'Destination Port'},
        {name: 'Length'},
        {name: 'Checksum', children: [{name: 'Calculated Checksum'}]},
        {name: 'Checksum Status'},
        {name: 'Stream index'},
        {name: 'Timestamps', children: [ // For some reason this is a value???
          {name: 'Time since first frame'}, 
          {name: 'Time since previous frame'}]
        },
        {name: 'UDP payload'}
      ]
      return ord
    },
    BFD(bits) {
      let ord = [
        ...bits.slice(0, 3),
        {name: 'Message Flags', children: [...bits.slice(3)]},
        {name: 'Detect Time Multiplier'},
        {name: 'My Discriminator'},
        {name: 'Your Discriminator'},
        {name: 'Desired Min TX Interval'},
        {name: 'Required Min RX Interval'},
        {name: 'Required Min Echo Interval'},
        {name: 'Authentication', children: [
          {name: 'Authentication Length'},
          {name: 'Authentication Key ID'}
        ]},
        {name: 'Password'}
      ]
      return ord
    },
    IPV6(bits) {
      let ord = [
          bits[0],
          {name: bits[1].name, value: bits[1].value, children: [
              ...bits.slice(2, 4)
          ]},
          bits[4],
          {name: 'Payload Length'},
          {name: 'Next Header'},
          {name: 'Hop Limit'},
          {name: 'Source Address'},
          {name: 'Destination Address'}
      ]
      return ord
    },
    GRE(bits) {
      let ord = [
        {name: 'Flags and Version', children: [...bits]},
        {name: 'Protocol Type'},
        {name: 'Data', children: [
          {name: 'data'}, 
          {name: 'Length'}
        ]}
      ]
      return ord
    },
    TCP(bits) {
      let ord = [
        {name: 'Source Port'},
        {name: 'Destination Port'},
        {name: 'Stream index'},
        {name: 'TCP Segment Len'},
        {name: 'Sequence number'},
        {name: 'Sequence Number (raw)'},
        {name: 'Next Sequence Number'},
        {name: 'Acknowledgment Number'},
        {name: 'Acknowledgment number (raw)'},
        bits[0],
        {name: 'Flags', children: [
          ...bits.slice(1), 
          {name: 'TCP Flags'}
        ]},
        {name: 'Expert Info (Chat/Sequence)'},
        {name: 'Connection establish request (SYN)'},
        {name: 'Severity level'},
        {name: 'Group'},
        {name: 'Window'},
        {name: 'Calculated window size'},
        {name: 'Checksum', children: [
            {name: 'Calculated Cheksum'}
        ]},
        {name: 'Checksum Status'},
        {name: 'Urgent Pointer'},
        {name: 'Timestamps', children: [
          {name: 'Time since first frame in this TCP stream'},
          {name: 'Time since previous frame in this TCP stream'}
        ]},
      ]
      return ord
    }
  },
  mounted() {
    let obj = {}
    let bits = []
    let ord = []

    this.data.tshark_raw_summary.forEach(element => {
      let key = element.substring(0, element.indexOf(":"))
      let value = element.substring(element.indexOf(":") + 1).trim()
      // There are some annoying corner cases where
      // key is inside value
      if(!key){
        key = value
        //if(key.includes("(")) 
        //  key = key.substring(0, value.indexOf("("))
        //value = value.substring(value.indexOf("(") + 1, value.indexOf(")")).trim()
      }

      else if(key.includes(' =')) {
        let bit = {}
        bit.name = key
        bit.value = value
        bits.push(bit)
      }
      else obj[key] = value
    })
    if(this.data.tshark_name == 'TCP')
      console.log(this.data.tshark_raw_summary)
    ord = this[this.data.tshark_name](bits)

    for(const attr of ord){
      if(obj[attr.name]){
        attr.value = obj[attr.name]
        if(attr.children)
          for(const child of attr.children)
            if(child.name in obj) 
              child.value = obj[child.name]
      }
    }
    //console.log(ord)
    this.sortedData = ord
  }
}
</script>

<style>
.dropdown-title {
  cursor: pointer;
}
.collapse {
  /*list-style-type: none;*/
}
</style>
<template> 
  <div class="wrapper"> 
  <div v-if="data"> 
    <v-card> 
    <DropDown> 
      <template v-slot:title> 
      <v-card-title>
        {{ data.name }}
      </v-card-title> 
      <v-card-subtitle>
        {{ data.tshark_name }}
      </v-card-subtitle> 
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
                <div v-if="child.children">
                  <DropDown>
                    <template v-slot:title>
                      <code>{{ child.name }}: {{ child.value }} </code> 
                    </template>
                    <template v-slot:content>
                      <ul>
                        <li v-for="(nestedChild, key) in child.children" :key="key">
                          <code>{{ nestedChild.name }}: {{ nestedChild.value }}</code>
                        </li>
                      </ul>
                    </template>
                  </DropDown>
                </div>
                <div v-else>
                  <code>{{ child.name }}: {{ child.value }} </code> 
                </div>
              </li> 
              </ul> 
            </template> 
            </DropDown> 
          </div> 
          <div v-else-if="tshark.value"> 
            <li>{{ tshark.name }}: {{ tshark.value }}</li> 
          </div> 
          </div> 
        </ul> 
        </v-card-text> </code> 
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
        {name: 'FCS Status'},
        {name: 'Length'},
        {name: 'Expert Info*'}, // Asteriks means key is not static
        {name: 'Severity level'},
        {name: 'Group'}
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
      let ord = [
        {name: 'Source Port'},
        {name: 'Destination Port'},
        {name: 'Length'},
        {name: 'Checksum', children: [{name: 'Calculated Checksum'}]},
        {name: 'Checksum Status'},
        {name: 'Stream index'},
        {name: 'Timestamps', children: [ 
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
            {name: 'Calculated Checksum'}
        ]},
        {name: 'Checksum Status'},
        {name: 'Urgent Pointer'},
        {name: 'Timestamps', children: [
          {name: 'Time since first frame in this TCP stream'},
          {name: 'Time since previous frame in this TCP stream'}
        ]},
      ]
      return ord
    },
    DNS(bits, length, names) {
      let answers = []
      for(let i = 0; i < names.length - 1; i++) {
        if(i === 0) answers.push({name: names[i + 1].name, children: [
          {name: 'Name-' + i},
          {name: 'Type-' + i},
          {name: 'Class-' + i},
          {name: 'Time to live'},
          {name: 'Data length'},
          {name: 'Address'}
        ]})
        else answers.push({name: names[i + 1].name, children: [
          {name: 'Name-' + i},
          {name: 'Type-' + i},
          {name: 'Class-' + i},
          {name: 'Time to live-' + (i - 1)},
          {name: 'Data length-' + (i - 1)},
        ]})
      }
      //console.log(answers)
      let ord = [
        {name: 'Transaction ID'},
        {name: 'Flags', children: [...bits]},
        {name: 'Questions'},
        {name: 'Answer RRs'},
        {name: 'Authority RRs'},
        {name: 'Additional RRs'},
        {name: 'Queries', children: [{name: names[0].name, children: [
          {name: 'Name'},
          {name: 'Name Length'},
          {name: 'Label Count'},
          {name: 'Type'},
          {name: 'Class'}
        ]}]},
        {name: 'Answers', children: [...answers]},
        {name: 'Unsolicited'}
      ]
      return ord
    },
    PTP(bits) {
      let ord = [
        ...bits.slice(0, 5),
        {name: 'messageLength'},
        {name: 'subdomainNumber'},
        {name: 'Reserved'},
        {name: 'flags', children: [
          ...bits.slice(5)
        ]},
        {name: 'correction', children: [
          {name: 'correction: Ns'},
          {name: 'correctionSubNs'}
        ]},
        {name: 'Reserved'},
        {name: 'ClockIdentity'},
        {name: 'SourcePortID'},
        {name: 'sequenceId'},
        {name: 'control'},
        {name: 'logMessagePeriod'},
        {name: 'originTimestamp (seconds)'},
        {name: 'originTimestamp (nanoseconds)'}
      ]
      return ord
    },
    TELNET(bits, length) {
      let dataChildren = []
      for(let i = 0; i < length; i++)
        dataChildren.push({name: 'Data-' + i})

      let ord = [
        {name: 'Data', children: [...dataChildren]}
      ]
      return ord
    },
    ICMPV6(bits, length) {
      let ord = [
        {name: 'Type'},
        {name: 'Code'},
        {name: 'Checksum'},
        {name: 'Checksum Status'},
        {name: 'Reserved'},
        {name: 'Target Address'},
        {name: 'ICMPv6 Option*', children: [
          {name: 'Type-0'},
          {name: 'Length'},
          {name: 'Link-layer address'},
          {name: 'Source Link-layer address'}
        ]},
      ]
      return ord
    },
    IGMP() {
      let ord = [
        {name: 'IGMP Version'},
        {name: 'Type'},
        {name: 'Max Resp Time'},
        {name: 'Checksum'},
        {name: 'Checksum Status'},
        {name: 'Multicast Address'}
      ]
      return ord
    },
    WINSREPL() {
      let ord = [
        {name: 'Packet Size'},
        {name: 'Opcode'},
        {name: 'Assoc_Ctx'},
        {name: 'Message_Type'},
        {name: 'WREPL_START_ASSOCIATION', children: [
          {name: 'Assoc_Ctx'},
          {name: 'Minor Version'},
          {name: 'Major Version'}
        ]}
      ]
      return ord
    },
    TPKT() {
      let ord = [
        {name: 'Version'},
        {name: 'Reserved'},
        {name: 'Length'}
      ]
      return ord
    }
  },
  mounted() {
    let obj = {}
    let bits = []
    let ord = []
    let names = []
    //let index = 0
    let repeatingItems = 0
    let copy = this.data.tshark_raw_summary.slice()

    // Converts tshark data from list to an object
    this.data.tshark_raw_summary.forEach(element => {
      let key = element.substring(0, element.indexOf(":")).trim()
      let value = element.substring(element.indexOf(":") + 1).trim()
      // There are cases where keys repeat and they cant
      // be handled in the same way as in ETH
      if(key in obj && this.data.tshark_name !== 'ETH') {
        repeatingItems = this.data.tshark_raw_summary.filter(item => item.match('^' + key + ': ')).length 
        let index = repeatingItems - copy.filter(item => item.match('^' + key + ':')).length
        copy.splice(copy.indexOf(copy.filter(x => x.match('^' + key + ':'))[0]), 1)
        //console.log('[DEBUG]: ' + element + ' '+ index)
        key = key + '-' + index
      }

      // Looks for domain names
      if(
        key.split('').filter(x => x === '.').length &&
        key.split('').filter(x => x === '.').length < 5
      ) {
        console.log(key)
        names.push({name: key, value: value})
      }

      // Who named keys 'correction:' and 'correction: Ns:'??!?!?!?!
      if(element.split('').filter(x => x === ":").length === 2) {
        key = element.substring(0, element.lastIndexOf(":")).trim()
        value = element.substring(element.lastIndexOf(":") + 1).trim()
      }

      // There are some annoying corner cases where
      // key is inside value. This handles them
      else if(!key){
        key = value.trim()
        if(key.includes("(")) {
          key = key.substring(0, value.indexOf("(")).trim()
          value = value.substring(value.indexOf("(") + 1, value.indexOf(")")).trim()
        }
        // For some reason children don't render properly
        // when parent element has no value
        else value = " "
      }

      // Takes care of bits and flags
      else if(key.includes(' =')) {
        bits.push({name: key, value: value})
      }
      obj[key] = value
    })

    //console.log(this.data.tshark_raw_summary)
    console.log(obj)
    // Exectues function that match tshark's name
    ord = this[this.data.tshark_name](bits, repeatingItems - 1, names)

    for(const attr of ord){
      // Handles non-static keys
      if(attr.name.includes('*')){
        const name = attr.name.slice(0, attr.name.indexOf('*'))
        let index = Object.keys(obj).findIndex((el) => {
          return el.match(name)
        })
        attr.name = Object.keys(obj)[index]
        attr.value = ord[Object.keys(obj)[index]]
      }

      // Assigns value to items and its children
      if(obj[attr.name])
        attr.value = obj[attr.name]
        if(attr.children)
          for(const child of attr.children)
            if(obj[child.name]) {
              child.value = obj[child.name]
              if(child.children)
                for(const nestedChild of child.children)
                  nestedChild.value = obj[nestedChild.name]
            }
    }
    console.log(ord)
    this.sortedData = ord
  }
}
</script>

<style>
.DropDown-title {
  cursor: pointer;
}
.collapse {
  list-style-type: none;
  margin-left: -15px;
}
.collapse::before {
  content: '\27A4 '
}
</style>
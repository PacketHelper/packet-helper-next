<template>
  <div class="wrapper">
    <v-card>
      <DropDown>
        <template v-slot:title>
          <v-card-title> {{ data.name }} </v-card-title>
          <v-card-subtitle> {{ data.tshark_name }} </v-card-subtitle>
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
                      <li><code>{{ data.repr }}</code></li>
                    </ul>
                  </template>
                </DropDown>
                <div v-if="sortedData">
                  <div
                    class="raw-data"
                    v-for="(tshark, key) in sortedData"
                    :key="key"
                  >
                    <div v-if="tshark.children">
                      <DropDown>
                        <template v-slot:title>
                          <li class="collapse">
                            {{ tshark.name }}: {{ tshark.value }}
                          </li>
                        </template>
                        <template v-slot:content>
                          <ul>
                            <li
                              v-for="(child, key) in tshark.children"
                              :key="key"
                            >
                              <div v-if="child.children">
                                <DropDown>
                                  <template v-slot:title>
                                    <code
                                      >{{ child.name }}: {{ child.value }}
                                    </code>
                                  </template>
                                  <template v-slot:content>
                                    <ul>
                                      <li
                                        v-for="(nestedChild, key) in child.children"
                                        :key="key"
                                      >
                                        <code
                                          >{{ nestedChild.name }}: {{
                                          nestedChild.value }}</code
                                        >
                                      </li>
                                    </ul>
                                  </template>
                                </DropDown>
                              </div>
                              <div v-else>
                                <code
                                  >{{ child.name }}: {{ child.value }}
                                </code>
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
                </div>
                <div v-else>
                  <li
                    v-for="(tshark, key) in data.tshark_raw_summary"
                    :key="key"
                  >
                    {{ tshark }}
                  </li>
                </div>
              </ul>
            </v-card-text>
          </code>
        </template>
      </DropDown>
    </v-card>
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
      sortedData: null,
      supported: true
    }
  },
  methods: {
    ETH(bits) {
      let ord = [
        {name: 'Destination', children: [
          {name: 'Address'},
          ...bits.slice(0,2)
        ]}, 
        {name: 'Source', children: [
          {name: 'Address'},
          ...bits.slice(2, 4)
        ]}, // {name: 'Address', value: addresses[1]}
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
        {name: 'Fragment Offset'},
        {name: 'Time to Live'},
        {name: 'Header Checksum', children: [{name: 'Calculated Checksum'}]},
        {name: 'Header checksum status'},
        {name: 'Source Address'},
        {name: 'Destination Address'}
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
          ...bits.slice(1, 6), 
          {name: 'TCP Flags'}
        ]},
        {name: 'TCP Segment Len'},
        {name: 'Expert Info'},
        {name: 'Connection establish request (SYN)'},
        {name: 'Severity level'},
        {name: 'Group'},
        {name: 'Window', children: [
          {name: 'Calculated window size'},
          {name: 'Window size scaling factor'}
        ]},
        {name: 'Calculated window size'},
        {name: 'Checksum', children: [
            {name: 'Calculated Checksum'}
        ]},
        {name: 'Checksum Status'},
        {name: 'Urgent Pointer'},
        {name: 'Options', children: [
          {name: 'TCP Option - No-Operation', children: [
            {name: 'Kind'}
          ]},
          {name: 'TCP Option - No-Operation', children: [
            {name: 'Kind'}
          ]},
          {name: 'TCP Option - Timestamps', children: [
            {name: 'Kind'},
            {name: 'Length'},
            {name: 'Timestamp value'},
            {name: 'Timestamp echo reply'}
          ]},
        ]},
        {name: 'SEQ/ACK analysis', children: [
          {name: 'Bytes in flight'},
          {name: 'Bytes sent since last PSH flag'}
        ]},
        {name: 'Timestamps', children: [
          {name: 'Time since first frame in this TCP stream'},
          {name: 'Time since previous frame in this TCP stream'}
        ]},
        {name: 'TCP payload'},
      ]
      return ord
    },
    DNS(bits, length, names) {
      let answers = []
      let nameservers = []
      for(let i = 0; i < names.length - 1; i++) {
        console.log(names[i + 1].value)
        if(names[i + 1].value.includes('type NS')) {
          nameservers.push({name: names[i + 1].name, children: [
            {name: 'Name'},
            {name: 'Type'},
            {name: 'Class'},
            {name: 'Time to live'},
            {name: 'Data length'},
            {name: 'Name Server'}
          ]})
        }
        else {
          answers.push({name: names[i + 1].name, children: [
            {name: 'Name'},
            {name: 'Type'},
            {name: 'Class'},
            {name: 'Time to live'},
            {name: 'Data length'},
          ]})
          if(names[i + 1].value.includes('addr'))
            answers[answers.length - 1].children.push({name: 'Address'})
          else if(names[i + 1].value.includes('type CNAME'))
            answers[answers.length - 1].children.push({name: 'CNAME'})
          }
        }
      //console.log(answers)
      let ord = [
        {name: 'Transaction ID'},
        {name: 'Flags', children: [...bits.slice(0, 6)]},
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
        {name: 'Authorative nameservers', children: [...nameservers]},
        {name: 'Unsolicited'},
        {name: 'Additional records', children: [
          {name: '<Root>', children: [
            {name: 'Type'},
            {name: 'UDP payload size'},
            {name: 'Higher bits in extended RCODE'},
            {name: 'EDNS0 version'},
            {name: 'Z', children: [...bits.slice(6)]}, // Needs one more loop in html but I think I will leave it at that
            {name: 'Data length'},
          ]}
        ]},
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
        dataChildren.push({name: 'Data'})

      let ord = [
        {name: 'Data', children: [...dataChildren]}
      ]
      return ord
    },
    ICMPV6(bits, length) {
      let ord = [
        {name: 'Type', children: [
          {name: 'Multicast Address'},
          {name: 'Multicast Address Record Changed to include'},
          {name: 'Number of Multicast Address Records'},
          {name: 'Number of Sources'},
          {name: 'Record Type'},
        ]},
        {name: 'Code'},
        {name: 'Checksum'},
        {name: 'Checksum Status'},
        {name: 'Reserved'},
        {name: 'Target Address'},
        {name: 'ICMPv6 Option', children: [
          {name: 'Type'},
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
    },
    QUIC(bits) {
      let ord = [
        ...bits,
        {name: 'Destination Connection ID'},
        {name: 'Destination Connection Length'},
        {name: 'Expert Info*'},
        {name: 'Group'},
        {name: 'Group'},
        {name: 'Length'},
        {name: 'Remaining Payload'},
        {name: 'Severity level'},
        {name: 'Severity level-0'},
        {name: 'Source Connection ID'},
        {name: 'Source Connection ID Length'},
        {name: 'Version'}
      ]
      return ord
    },
    TLS() {
      let ord = [
        {name: 'Application Data Protocol'},
        {name: 'Content Type'},
        {name: 'Encrypted Application Data'},
        {name: 'Length'},
        {name: 'TLSv1.2 Record Layer: Application Data Protocol'},
        {name: 'Version'}
      ]
      return ord
    },
    HTTP() {
      let ord = [
        {name: 'Connection'},
        {name: 'HTTP response'},
        {name: 'HTTP/1.1', children: [
          {name: 'Expert Info', children: [
            {name: 'HTTP/1.1'},
            {name: 'Severity level'},
            {name: 'Group'}
          ]},
          {name: 'Response Version'},
          {name: 'Status Code'},
          {name: 'Status Code Description'},
          {name: 'Response Phrase'}
        ]},
        {name: 'Date'},
        {name: 'Server'},
        {name: 'Connection'},
        {name: 'Keep-Alive'},
        {name: 'ETag'},
      ]
      return ord
    },
    TLS() {
      let ord = [
        {name: 'TLSv1.', children: [
          {name: 'Content Type'},
          {name: 'Version'},
          {name: 'Length'},
          {name: 'Encrypted Application Data'},
          {name: 'Application Data Protocol'}
        ]}
      ]
      return ord
    },
    SSDP() {
      let ord = [
        {name: 'NOTIFY * HTTP', children: [
          {name: 'Expert Info', children: [
            {name: 'NOTIFY * HTTP'},
            {name: 'Severity level'},
            {name: 'Group'}
          ]},
          {name: 'Request Method'},
          {name: 'Request URI'},
          {name: 'Request Version'}
        ]},
        {name: 'HOST'},
        {name: 'CACHE-CONTROl'},
        {name: 'LOCATION'},
        {name: 'NT'},
        {name: 'NTS'},
        {name: 'SERVER'},
        {name: 'USN'},
        {name: 'Full request'}
      ]
      return ord
    }
  },
  mounted() {
    // When protocol is not supported, don't do anything
    if(!this[this.data.tshark_name]) return
    let copy = this.data.tshark_raw_summary.slice() 
    //console.log(this.data.tshark_raw_summary)
    let bits = []
    let names = []

    // Prepare arrays for bits and DNS nameservers
    copy.forEach(element => {
      if(element.includes(' =')){
        bits.push({
          name: element.substring(0, element.indexOf(':')),
          value: element.substring(element.indexOf(':') + 1),
        })
      }
      // if key has dots and there are less than 4 of them
      // ex.: www.youtube.com
      else if(element.substring(0, element.indexOf(':')).split('.').length - 1 && 
         element.substring(0, element.indexOf(':')).split('.').length - 1 < 4) {
        names.push({
          name: element.substring(0, element.indexOf(':')),
          value: element.substring(element.indexOf(':') + 1),
        })
      }})

    // Executes function that coresponds to tshark's name
    let ord = this[this.data.tshark_name](bits, 4, names)

    // Insert values into final object
    ord.forEach(element => {
      let re_parent = new RegExp('^' + element.name)
      let index_parent = copy.findIndex(el => re_parent.test(el))
      if(index_parent !== -1) {
        element.value = copy[index_parent].substring(copy[index_parent].indexOf(':') + 1).trim()
        // Remove processed item to avoid duplicates
        copy.splice(index_parent, 1)
      }

      if(element.children)
        element.children.forEach(child => {
          let re_child = new RegExp('^' + child.name + ':')
          let index_child = copy.findIndex(el => re_child.test(el))
          if(index_child !== -1) {
            child.value = copy[index_child].substring(copy[index_child].indexOf(':') + 1).trim()
            copy.splice(index_child, 1)
          }

          if(child.children) {
            child.children.forEach(nested_child => {
              let re_nested_child = new RegExp('^' + nested_child.name + ':')
              let index_nested_child = copy.findIndex(el => 
              re_nested_child.test(el))
              if(index_nested_child !== -1) {
                nested_child.value = copy[index_nested_child].substring(copy[index_nested_child].indexOf(':') + 1).trim()
                copy.splice(index_nested_child, 1)
              }
            })
          }
        })
    })
    console.log(ord)
    // Finally display the data
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
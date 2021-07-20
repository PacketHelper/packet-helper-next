export default {
  ETH(bits) {
    let ord = [
      {
        name: "Destination",
        children: [{ name: "Address" }, ...bits.slice(0, 2)],
      },
      {
        name: "Source",
        children: [{ name: "Address" }, ...bits.slice(2, 4)],
      },
      { name: "Type" },
      { name: "Frame check sequence" },
      { name: "FCS Status" },
      { name: "Length" },
      { name: "Expert Info" },
      { name: "Severity level" },
      { name: "Group" },
    ];
    return ord;
  },
  IP(bits) {
    let ord = [
      ...bits.slice(0, 1),
      {
        name: "Differentiated Services Field",
        children: [...bits.slice(2, 4)],
      },
      { name: "Total Length" },
      { name: "Identification" },
      { name: "Flags", children: [...bits.slice(4)] },
      { name: "Time to live" },
      { name: "Protocol" },
      { name: "Fragment Offset" },
      { name: "Time to Live" },
      { name: "Header Checksum", children: [{ name: "Calculated Checksum" }] },
      { name: "Header checksum status" },
      { name: "Source Address" },
      { name: "Destination Address" },
    ];
    return ord;
  },
  UDP() {
    let ord = [
      { name: "Source Port" },
      { name: "Destination Port" },
      { name: "Length" },
      { name: "Checksum", children: [{ name: "Calculated Checksum" }] },
      { name: "Checksum Status" },
      { name: "Stream index" },
      {
        name: "Timestamps",
        children: [
          { name: "Time since first frame" },
          { name: "Time since previous frame" },
        ],
      },
      { name: "UDP payload" },
    ];
    return ord;
  },
  BFD(bits) {
    let ord = [
      ...bits.slice(0, 3),
      { name: "Message Flags", children: [...bits.slice(3)] },
      { name: "Detect Time Multiplier" },
      { name: "My Discriminator" },
      { name: "Your Discriminator" },
      { name: "Desired Min TX Interval" },
      { name: "Required Min RX Interval" },
      { name: "Required Min Echo Interval" },
      {
        name: "Authentication",
        children: [
          { name: "Authentication Length" },
          { name: "Authentication Key ID" },
        ],
      },
      { name: "Password" },
    ];
    return ord;
  },
  IPV6(bits) {
    let ord = [
      { name: "Expert Info" },
      bits[0],
      {
        name: bits[1].name,
        value: bits[1].value,
        children: [...bits.slice(2, 4)],
      },
      bits[4],
      { name: "Payload Length" },
      { name: "Next Header" },
      { name: "Hop Limit" },
      { name: "Source Address" },
      { name: "Destination Address" },
    ];
    return ord;
  },
  GRE(bits) {
    let ord = [
      { name: "Flags and Version", children: [...bits] },
      { name: "Protocol Type" },
      {
        name: "Data",
        children: [{ name: "data" }, { name: "Length" }],
      },
    ];
    return ord;
  },
  TCP(bits, length, names, options) {
    let processedOptions = [];

    options.forEach((element) => {
      let temp = {
        name: element,
        children: [{ name: "Kind" }],
      };
      if (element.includes("Timestamps")) {
        temp.children.push({ name: "Length" });
        temp.children.push({ name: "Timestamp value" });
        temp.children.push({ name: "Timestamp echo reply" });
      } else if (element.includes("Maximum segment size")) {
        temp.children.push({ name: "Length" });
        temp.children.push({ name: "MSS Value" });
      } else if (element.includes("SACK permitted")) {
        temp.children.push({ name: "Length" });
      }
      processedOptions.push(temp);
    });
    processedOptions.sort((a, b) => {
      return a.name > b.name;
    });

    let ord = [
      { name: "Source Port" },
      { name: "Destination Port" },
      { name: "Stream index" },
      { name: "TCP Segment Len" },
      { name: "Sequence number" },
      { name: "Sequence Number (raw)" },
      { name: "Next Sequence Number" },
      { name: "Acknowledgment Number" },
      { name: "Acknowledgment number (raw)" },
      bits[0],
      {
        name: "Flags",
        children: [...bits.slice(1), { name: "TCP Flags" }],
      },
      { name: "TCP Segment Len" },
      { name: "Expert Info" },
      { name: "Connection establish request (SYN)" },
      { name: "Severity level" },
      { name: "Group" },
      {
        name: "Window",
        children: [
          { name: "Calculated window size" },
          { name: "Window size scaling factor" },
        ],
      },
      { name: "Calculated window size" },
      {
        name: "Checksum",
        children: [{ name: "Calculated Checksum" }],
      },
      { name: "Checksum Status" },
      { name: "Urgent Pointer" },
      { name: "Options", children: [...processedOptions] },
      {
        name: "SEQ/ACK analysis",
        children: [
          { name: "Bytes in flight" },
          { name: "Bytes sent since last PSH flag" },
        ],
      },
      {
        name: "Timestamps",
        children: [
          { name: "Time since first frame in this TCP stream" },
          { name: "Time since previous frame in this TCP stream" },
        ],
      },
      { name: "TCP payload" },
    ];
    return ord;
  },
  DNS(bits, length, names) {
    let answers = [];
    let nameservers = [];
    for (let i = 0; i < names.length - 1; i++) {
      if (names[i + 1].value.includes("type NS")) {
        nameservers.push({
          name: names[i + 1].name,
          children: [
            { name: "Name" },
            { name: "Type" },
            { name: "Class" },
            { name: "Time to live" },
            { name: "Data length" },
            { name: "Name Server" },
          ],
        });
      } else {
        answers.push({
          name: names[i + 1].name,
          children: [
            { name: "Name" },
            { name: "Type" },
            { name: "Class" },
            { name: "Time to live" },
            { name: "Data length" },
          ],
        });
        if (names[i + 1].value.includes("addr"))
          answers[answers.length - 1].children.push({ name: "Address" });
        else if (names[i + 1].value.includes("type CNAME"))
          answers[answers.length - 1].children.push({ name: "CNAME" });
      }
    }
    //console.log(answers)
    let ord = [
      { name: "Transaction ID" },
      { name: "Flags", children: [...bits.slice(0, 10)] },
      { name: "Questions" },
      { name: "Answer RRs" },
      { name: "Authority RRs" },
      { name: "Additional RRs" },
      {
        name: "Queries",
        children: [
          {
            name: names[0].name,
            children: [
              { name: "Name" },
              { name: "Name Length" },
              { name: "Label Count" },
              { name: "Type" },
              { name: "Class" },
            ],
          },
        ],
      },
      { name: "Answers", children: [...answers] },
      { name: "Authorative nameservers", children: [...nameservers] },
      { name: "Unsolicited" },
      {
        name: "Additional records",
        children: [
          {
            name: "<Root>",
            children: [
              { name: "Type" },
              { name: "UDP payload size" },
              { name: "Higher bits in extended RCODE" },
              { name: "EDNS0 version" },
              { name: "Z" }, // Needs one more loop in html but I think I will leave it at that
              ...bits.slice(10),
              { name: "Data length" },
            ],
          },
        ],
      },
    ];
    return ord;
  },
  PTP(bits) {
    let ord = [
      ...bits.slice(0, 5),
      { name: "messageLength" },
      { name: "subdomainNumber" },
      { name: "Reserved" },
      {
        name: "flags",
        children: [...bits.slice(5)],
      },
      {
        name: "correction",
        children: [{ name: "correction: Ns" }, { name: "correctionSubNs" }],
      },
      { name: "Reserved" },
      { name: "ClockIdentity" },
      { name: "SourcePortID" },
      { name: "sequenceId" },
      { name: "control" },
      { name: "logMessagePeriod" },
      { name: "originTimestamp (seconds)" },
      { name: "originTimestamp (nanoseconds)" },
    ];
    return ord;
  },
  TELNET(bits, length) {
    let dataChildren = [];
    for (let i = 0; i < length - 1; i++) dataChildren.push({ name: "Data" });

    let ord = [{ name: "Data", children: [...dataChildren] }];
    return ord;
  },
  ICMPV6(bits, length) {
    let ord = [
      {
        name: "Type",
        children: [
          { name: "Multicast Address" },
          { name: "Multicast Address Record Changed to include" },
          { name: "Number of Multicast Address Records" },
          { name: "Number of Sources" },
          { name: "Record Type" },
        ],
      },
      { name: "Code" },
      { name: "Checksum" },
      { name: "Checksum Status" },
      { name: "Reserved" },
      { name: "Target Address" },
      {
        name: "ICMPv6 Option",
        children: [
          { name: "Type" },
          { name: "Length" },
          { name: "Link-layer address" },
          { name: "Source Link-layer address" },
        ],
      },
    ];
    return ord;
  },
  IGMP() {
    let ord = [
      { name: "IGMP Version" },
      { name: "Type" },
      { name: "Max Resp Time" },
      { name: "Checksum" },
      { name: "Checksum Status" },
      { name: "Multicast Address" },
    ];
    return ord;
  },
  WINSREPL() {
    let ord = [
      { name: "Packet Size" },
      { name: "Opcode" },
      { name: "Assoc_Ctx" },
      { name: "Message_Type" },
      {
        name: "WREPL_START_ASSOCIATION",
        children: [
          { name: "Assoc_Ctx" },
          { name: "Minor Version" },
          { name: "Major Version" },
        ],
      },
    ];
    return ord;
  },
  TPKT() {
    let ord = [{ name: "Version" }, { name: "Reserved" }, { name: "Length" }];
    return ord;
  },
  QUIC(bits) {
    let ord = [
      ...bits,
      { name: "Destination Connection ID" },
      { name: "Destination Connection Length" },
      { name: "Expert Info" },
      { name: "Group" },
      { name: "Group" },
      { name: "Length" },
      { name: "Remaining Payload" },
      { name: "Severity level" },
      { name: "Severity level" },
      { name: "Source Connection ID" },
      { name: "Source Connection ID Length" },
      { name: "Version" },
    ];
    return ord;
  },
  TLS() {
    let ord = [
      { name: "Application Data Protocol" },
      { name: "Content Type" },
      { name: "Encrypted Application Data" },
      { name: "Length" },
      { name: "TLSv1.2 Record Layer: Application Data Protocol" },
      { name: "Version" },
    ];
    return ord;
  },
  HTTP() {
    let ord = [
      { name: "Connection" },
      { name: "HTTP response" },
      {
        name: "HTTP/1.1",
        children: [
          {
            name: "Expert Info",
            children: [
              { name: "HTTP/1.1" },
              { name: "Severity level" },
              { name: "Group" },
            ],
          },
          { name: "Response Version" },
          { name: "Status Code" },
          { name: "Status Code Description" },
          { name: "Response Phrase" },
        ],
      },
      { name: "Date" },
      { name: "Server" },
      { name: "Connection" },
      { name: "Keep-Alive" },
      { name: "ETag" },
    ];
    return ord;
  },
  TLS() {
    let ord = [
      {
        name: "TLSv1.",
        children: [
          { name: "Content Type" },
          { name: "Version" },
          { name: "Length" },
          { name: "Encrypted Application Data" },
          { name: "Application Data Protocol" },
        ],
      },
    ];
    return ord;
  },
  SSDP() {
    let ord = [
      {
        name: "NOTIFY * HTTP",
        children: [
          {
            name: "Expert Info",
            children: [
              { name: "NOTIFY * HTTP" },
              { name: "Severity level" },
              { name: "Group" },
            ],
          },
          { name: "Request Method" },
          { name: "Request URI" },
          { name: "Request Version" },
        ],
      },
      { name: "HOST" },
      { name: "CACHE-CONTROl" },
      { name: "LOCATION" },
      { name: "NT" },
      { name: "NTS" },
      { name: "SERVER" },
      { name: "USN" },
      { name: "Full request" },
    ];
    return ord;
  },
};

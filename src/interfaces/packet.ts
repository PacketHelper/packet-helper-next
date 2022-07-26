export default interface Packet {
  name: string;
  scapy_name: string;
}

export interface StructureChksumStatus {
  chksum: string;
  chksum_calculated: string;
  status: boolean | null;
}

export interface Structure {
  name: string;
  bytes: string;
  hex: string;
  hex_one: string;
  length: number;
  repr: string;
  repr_full: string;
  tshark_name: string;
  tshart_raw_summary: string[];
  chksum_status: StructureChksumStatus;
}

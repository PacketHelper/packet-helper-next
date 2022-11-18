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
  bytes_record: string;
  hex_record: string;
  hex_record_full: string;
  length: number;
  length_unit: string;
  representation: string;
  representation_full: string;
  tshark_name: string;
  tshark_raw_summary: string[];
  chksum_status: StructureChksumStatus;
}

import api from "@/services/api";

export default {
  async getHex(hex_string: string) {
    const response = await api.get(`hex/${hex_string}`);
    return response.data;
  },
  async getInfo() {
    const response = await api.get(`info`);
    return response.data;
  },
  async getScapy(protocols: Array<string>) {
    return await api
      .post(`packets`, { packets: protocols })
      .then((response) => response.data["packets"]);
  },
  async createPacket(packetInfo: Array<any>) {
    return await api
      .post(`create`, { packets: packetInfo })
      .then((response) => response.data["builtpacket"]);
  },
};

import api from "@/services/api";

export default {
  getHex(hex_string) {
    return api.get(`hex/${hex_string}`).then((response) => response.data);
  },
  getInfo() {
    return api.get(`info`).then((response) => response.data);
  },
  getScapy(protocols) {
    return api.post(`packets`, protocols).then((response) => response.data);
  },
  createPacket(packetInfo) {
    return api.post(`create`, packetInfo).then((response) => response.data);
  },
};

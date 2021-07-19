import api from "@/services/api";

export default {
  getHex(hex_string) {
    return api.get(`hex/${hex_string}`).then((response) => response.data);
  },
  getInfo() {
    return api.get(`info`).then((response) => response.data);
  },
};

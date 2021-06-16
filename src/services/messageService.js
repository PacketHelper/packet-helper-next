import api from '@/services/api'

export default {
    fetchMessages() {
        return api.get(`messages/`)
            .then(response => response.data)
    },
    postMessage(payload) {
        return api.post(`messages/`, payload)
            .then(response => response.data)
    },
    deleteMessage(msgId) {
        return api.delete(`messages/${msgId}`)
            .then(response => response.data)
    },
    getHex(hex_string) {
        return api.get(`hex/${hex_string}`)
            .then(response => response.data);
    },
    getInfo() {
        return api.get(`info`)
            .then(response => response.data);
    }
}
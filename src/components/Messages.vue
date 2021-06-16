<template>
  <div class="hello">
    <img src='@/assets/logo-django.png' style="width: 250px"/>
    <p>The data below is added/removed from the SQLite Database using Django's ORM and Rest Framework.</p>
    <br/>
    <p>Subject</p>
    <input type="text" placeholder="Hello" v-model="subject">
    <p>Message</p>
    <input type="text" placeholder="From the other side" v-model="msgBody">
    <br>
    <input type="text" placeholder="ff00" v-model="hex">
    <input type="submit" value="Hex" @click="getHex(hex)"/>
    <br>
    <input
        type="submit"
        value="Add"
        @click="addMessage({ subject: subject, body: msgBody })"
        :disabled="!subject || !msgBody">

    <hr/>
    <h3>Messages on Database</h3>
    <p v-if="messages.length === 0">No Messages</p>
    <div class="msg" v-for="(msg, index) in messages" :key="index">
      <p class="msg-index">[{{ index }}]</p>
      <p class="msg-subject" v-html="msg.subject"></p>
      <p class="msg-body" v-html="msg.body"></p>
      <input type="submit" @click="deleteMessage(msg.pk)" value="Delete"/>
    </div>
  </div>
</template>

<script>
import {mapActions, mapState} from 'vuex'
import MessageService from "../services/messageService.js"

export default {
  name: "Messages",
  data() {
    return {
      subject: "",
      msgBody: "",
      hex: ""
    };
  },
  computed: mapState({
    messages: state => state.messages.messages
  }),
  methods: {
    ...mapActions('messages', [
          'addMessage',
          'deleteMessage',
        ],
    ),
    async getHex(hex_string) {
      let message = await MessageService.getHex(hex_string);
      message.name
      // console.log(message);
    }
  },

  created() {
    this.$store.dispatch('messages/getMessages')
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
hr {
  max-width: 65%;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

</style>

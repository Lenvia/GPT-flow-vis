<template>
  <div class="message" :class="`message-${sender}`">
    <div class="message-content">{{ content }}</div>
    <div class="message-sender">{{ sender }}</div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Message',
  props: {
    content: {
      type: String,
      required: true,
    },
    sender: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped>

.message {
  margin: 5px;
  padding: 5px;
  border-radius: 5px;
}
.message-content {
  font-size: 14px;
}
.message-sender {
  font-size: 10px;
  color: gray;
}
.message-me {
  background-color: #00cc00;
  color: white;
}
.message-system {
  background-color: #E4E7ED;
  color: black;
}


</style>
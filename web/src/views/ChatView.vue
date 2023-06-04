<template>
  <div class="full-size">
    <el-row class="full-size flex_column">
      <el-row class="full-width bg-color-aquamarine content_center" style="height: 20%">
        <div style="height: 40%; width: 60%; display: flex">
          <el-input v-model="areaInput"
                    clearable
                    :rows="4"
                    maxlength="100"
                    type="textarea"
                    @keydown.enter.prevent="handleEnter"
          />
          <el-upload
              class="upload-demo"
              :action="''"
              :limit="1"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleChange"
          >
            <el-button type="primary">select file
              <el-icon class="el-icon--right">
                <Upload/>
              </el-icon>
            </el-button>
          </el-upload>


          <el-button type="primary" round @click="submit">Submit</el-button>
        </div>
      </el-row>

      <el-row class="full-width flex_row" style="height: 80%">
        <el-col class="full-height" :span="14">
          <div class="full-size" style="background-color: black;">
            <img :src="`data:image/png;base64,${imgSrc}`" :style="{ width: '100%', height: '60%' }" alt="streamline"/>

            <el-input
                type="textarea"
                :rows="13"
                v-model="dataset_info"
                readonly
                style="height:38%; overflow-y: auto;"></el-input>
          </div>


        </el-col>

        <el-col class="full-height" :span="10">
          <div class="full-size bg-color-aliceblue">
            <el-card class="chat-box">
              <div class="messages">
                <Message v-for="(message, index) in messages" :key="index" :content="message.content"
                         :role="message.role"/>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </el-row>

  </div>
</template>

<script lang="ts">
import {ElInput, ElCol, ElRow, ElCard, ElButton, ElUpload, ElIcon} from 'element-plus'
import {Upload} from '@element-plus/icons-vue'

import {ref, onMounted, getCurrentInstance, onUnmounted} from 'vue'
import {useWebSocket} from "@/plugin/websocket";
import http from '@/plugin/request';
import emitter from "@/bus";
import Message from '@/components/Message.vue';

const areaInput = ref('')
const fileName = ref('');
const messages = ref([
  {content: '欢迎加入', role: 'system'},
]);


export default {
  name: "ChatView",
  components: {ElInput, ElCol, ElRow, ElCard, ElButton, ElUpload, Upload, ElIcon, Message},

  created() {
    const instance = getCurrentInstance();
    console.log(instance)
  },

  setup() {

    const dataset_info = ref('')

    const {ws} = useWebSocket()

    const imgSrc = ref('');

    const handleChange = async (file: File) => {
      fileName.value = file.name;
      const response = await http.post('/upload/', {
        "file_name": fileName.value,
      }, {
        timeout: 20000
      })

      dataset_info.value = response.data
    };

    function submit() {
      console.log("发送消息： ", areaInput.value)
      ws.value?.send(areaInput.value);

      messages.value.push({
        content: areaInput.value,
        role: "me",
      })
    }

    const flushPicHandler = (e: unknown) => {
      let event = e as { base64ImageData: string };
      imgSrc.value = event.base64ImageData;
    };

    const addChatMessage = (e: unknown) =>{
      let event = e as {role: string, content: string};
      messages.value.push({
        content: event.content,
        role: event.role,
      })
    }

    const handleEnter = (event: KeyboardEvent) => {
      // 处理 Enter 键按下事件
      if (event.metaKey || event.ctrlKey || event.shiftKey) { // 检查是否按下 Command 或 Ctrl 或 Shift
        // 换行逻辑，可以根据需要自行实现
        event.preventDefault(); // 阻止默认的换行行为
        areaInput.value += '\n'
      } else {
        // 发送消息逻辑
        submit();
      }
    };

    onMounted(() => {
      emitter.on('flush_pic', flushPicHandler);
      emitter.on('message', addChatMessage);
    });

    onUnmounted(() => {
      emitter.off('flush_pic', flushPicHandler);
    });

    return {
      areaInput,
      submit,
      handleEnter,
      fileName,
      handleChange,
      imgSrc,
      dataset_info,
      messages,
    }
  }
}

</script>

<style scoped>
.upload-demo {
  display: inline-block;
  margin-right: 10px;
}

.chat-box {
  width: 100%;
  height: 50%;
  overflow-y: auto;
}
</style>
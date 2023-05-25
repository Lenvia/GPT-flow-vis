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
        <el-col class="full-height" :span="16">
          <div class="full-size bg-color-aqua">123</div>
        </el-col>

        <el-col class="full-height" :span="8">
          <div class="full-size bg-color-aliceblue">456</div>
        </el-col>
      </el-row>
    </el-row>

  </div>
</template>

<script lang="ts">
import {ElInput, ElCol, ElRow, ElButton, ElUpload, ElIcon} from 'element-plus'
import {Upload} from '@element-plus/icons-vue'

import {ref, onMounted, getCurrentInstance} from 'vue'
import {dialog} from 'electron';
import path from 'path';
import {useWebSocket} from "@/plugin/websocket";
import http from '@/utils/request';

const areaInput = ref('')
const fileName = ref('');

export default {
  name: "ChatView",
  components: {ElInput, ElCol, ElRow, ElButton, ElUpload, Upload, ElIcon},

  created() {
    const instance = getCurrentInstance();
    console.log(instance)
  },

  setup() {

    const {ws} = useWebSocket()
    // const csrftoken = getCookie('csrftoken');
    // console.log(csrftoken)
    //
    // // 获取 CSRF token
    // function getCookie(name: string) {
    //   const value = `; ${document.cookie}`;
    //   const parts = value.split(`; ${name}=`);
    //   if (parts.length === 2) {
    //     return parts.pop()?.split(';').shift();
    //   }
    // }

    const handleChange = async (file: File) => {
      fileName.value = file.name;
      const response = await http.post('/upload/', {
        "file_name": fileName.value,
      }, {
        timeout: 20000
      })

      console.log(response.data)
    };

    // const selectFile = () => {
    //   dialog.showOpenDialog({properties: ['openFile']}).then((result) => {
    //     if (!result.canceled && result.filePaths.length > 0) {
    //       const file = result.filePaths[0];
    //       const absolutePath = path.resolve(file);
    //       filePath.value = absolutePath;
    //       console.log(filePath.value)
    //     }
    //   }).catch((err) => {
    //     console.error(err);
    //   });
    // };

    function submit() {
      console.log(areaInput.value)
      ws.value?.send(areaInput.value);
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

    return {
      areaInput,
      submit,
      handleEnter,
      fileName,
      handleChange
    }
  }
}

</script>

<style scoped>
.upload-demo {
  display: inline-block;
  margin-right: 10px;
}
</style>
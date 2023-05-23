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
          <!--          <el-upload-->
          <!--              class="upload-demo"-->
          <!--              :action="''"-->
          <!--              :limit="1"-->
          <!--              :auto-upload="false"-->
          <!--              :show-file-list="false"-->
          <!--              :on-change="handleChange"-->
          <!--          >-->
          <!--            <el-button type="primary">select file-->
          <!--              <el-icon class="el-icon&#45;&#45;right"><Upload /></el-icon></el-button>-->
          <!--          </el-upload>-->

<!--          <el-select v-model="selectedFile" class="m-2" placeholder="Select" size="large">-->
<!--            <el-option-->
<!--                v-for="fileName in fileNames"-->
<!--                :key="fileName"-->
<!--                :label="fileName"-->
<!--                :value="fileName"-->
<!--            />-->
<!--          </el-select>-->

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
// import fs from 'fs';
import {ref, onMounted} from 'vue'

const areaInput = ref('')

export default {
  name: "ChatView",
  components: {ElInput, ElCol, ElRow, ElButton, ElUpload, Upload, ElIcon},

  setup() {
    const fileNames = ref<string[]>([]);

    const selectedFile = ref('');

    // const loadFileNames = () => {
    //   const folderPath = 'Users/yy/GithubProjects/GPT-flow-vis/experiment/data/nc_flow_field'; // 替换成实际的文件夹路径
    //
    //   fs.readdir(folderPath, (err, files) => {
    //     if (err) {
    //       console.error(err);
    //       return;
    //     }
    //     fileNames.value = files;
    //   });
    // };
    //
    // onMounted(() => {
    //   loadFileNames();
    // });

    // const handleChange = (file: File) => {
    //   console.log(file)
    //   fileName.value = file.name;
    //   console.log(fileName.value)
    // };

    function submit() {
      console.log(areaInput.value)
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
      fileNames,
      selectedFile,
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
<template>
  <div class="full-size">
    <el-row class="full-size flex_column">
      <el-row class="full-width bg-color-aquamarine content_center" style="height: 20%">
        <div style="height: 40%; width: 80%; display: flex" >
        <el-input v-model="input" @change="handler(input)"
                  clearable
                  :rows="4"
                  maxlength="100"
                  type="textarea"
        />
        <el-button type="primary" round>Primary</el-button>
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
import {ElInput, ElCol, ElRow, ElButton} from 'element-plus'


import {ref} from 'vue'

const input = ref('')

export default {
  name: "ChatView",
  components: {ElInput, ElCol, ElRow, ElButton},

  setup() {

    function handler(input: string) {
      console.log(input)
    }

    return {
      input,
      handler,
    }
  }
}

</script>

<style scoped>
/deep/ .el-textarea__inner {
  width: 800px;
}

</style>
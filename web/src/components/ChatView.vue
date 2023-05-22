<template>
<div class="full-size bg-color-aquamarine">

  <el-row class="full-size flex_row bg-color-beige">

  </el-row>

  <el-input v-model="input" @change="handler(input)"
            clearable
            :rows="4"
            maxlength="100"
            type="textarea"
  ></el-input>
</div>
</template>

<script lang="ts">
import {ElInput} from 'element-plus'
import { ref } from 'vue'

const input = ref('')

export default {
  name: "ChatView",
  components:{ElInput},

  setup() {

    function handler(input: string){
      console.log(input)
    }

    return {
      input,
      handler
    }
  }
}

</script>

<style scoped>

</style>
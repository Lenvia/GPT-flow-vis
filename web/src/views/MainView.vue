<template>
  <div class="full-size">
    <el-row class="full-size flex_row bg-color-beige">
      <el-col class="full-height flex_column" :span="6" style="flex-grow: 1">
<!--        <div class="grid-content ep-bg-purple"/>-->
        <ChatView></ChatView>
      </el-col>

      <el-col class="full-height flex_column" :span="6" style="flex-grow: 1">
        <!--        <div class="grid-content ep-bg-purple-light"/>-->
        <div class="full-size bg-color-cadetblue" >111</div>
      </el-col>

      <el-col class="full-height flex_column" :span="6" style="flex-grow: 1">
<!--        <div class="grid-content ep-bg-purple-light"/>-->
        <div class="full-size bg-color-aliceblue" >222</div>
      </el-col>

    </el-row>
  </div>
</template>

<script lang="ts">
import {ElCol, ElRow} from 'element-plus'
import ChatView from "@/components/ChatView.vue";

export default {
  name: "MainView",
  components: {ChatView, ElCol, ElRow}
}
</script>

<style>

.full-size {
  height: 100%;
  width: 100%;
}

.full-height{
  height: 100%;
}

/* 父类标签如此设置，子标签可以通过 flex-grow 进行 高度划分*/
.flex_column {
  display: flex;
  flex-direction: column
}

.flex_row {
  display: flex;
  flex-direction: row;
}

.height_adjust_equal {
  flex-grow: 1;
}

/* 内容居中 */
.content_center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 内容仅垂直居中 */
.content_vertical_center {
  display: flex;
  align-items: center;
}


/*
  以下样式仅供dev
 */

.bg-color-aqua {
  background-color: aqua;
}

.bg-color-aliceblue {
  background-color: aliceblue;
}

.bg-color-beige {
  background-color: beige;
}

.bg-color-cadetblue {
  background-color: cadetblue;
}

.bg-color-aquamarine {
  background-color: aquamarine;
}

</style>

<style scoped>

</style>
<template>
  <div style="background-color: blueviolet; height: 98vh; width: 98vw">
    <el-row class="full-size flex_row bg-color-beige">
      <el-col class="full-height flex_column" :span="14" style="background-color: aliceblue; ">
        <ChatView></ChatView>
      </el-col>

      <el-col class="full-height  flex_column" :span="6">
        <!--        <div class="grid-content ep-bg-purple-light"/>-->
        <div class="full-size bg-color-cadetblue">111</div>
      </el-col>

      <el-col class="full-height  flex_column" :span="4">
        <div class="full-size bg-color-hotpink" >222</div>
      </el-col>

    </el-row>
  </div>

</template>

<script lang="ts">
import {ElCol, ElRow, ElDivider, ElCard} from 'element-plus'
import ChatView from "@/views/ChatView.vue";
import {defineComponent, onMounted, onUnmounted} from 'vue';
import {useWebSocket} from "@/plugin/websocket";
export default defineComponent({
  name: "MainView",
  props: {
    span: {
      type: Number,
      default: 24
    }
  },
  components: {ChatView, ElCol, ElRow, ElDivider, ElCard},

  // setup(){
  //
  // }


})
</script>

<style>

.full-size {
  height: 100%;
  width: 100%;
}

.full-height{
  height: 100%;

}

.full-width{
  width: 100%;
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

.flex-grow-one{
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

.bg-color-hotpink{
  background-color: hotpink;
}

</style>

<style scoped>
.lightgreen-box {
  background-color: lightgreen;
  height: 24px;
}
.orange-box {
  background-color: orange;
  height: 24px;
}
</style>
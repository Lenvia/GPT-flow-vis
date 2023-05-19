<template>
  <div>

  </div>
</template>

<script lang="ts">
import http from '@/utils/request';
import {onMounted} from "vue";




export default {
  name: "test",

  setup(){

    const test = async ()=>{
      try{
          const response = http.get('server/test/');
          console.log(response)
      } catch (error){
        console.log(error);
      }
    };

    onMounted(test)
  }

}
</script>

<style scoped>

</style>
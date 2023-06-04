import { ref, onMounted, onUnmounted } from 'vue'
import emitter from '../bus'

const wsUrl = 'ws://localhost:9900/ws/'

// 定义一个 WebSocket 的 Vue Composition API
export const useWebSocket = () => {
    const ws = ref<WebSocket | null>(null)

    const initWebSocket = () => {
        ws.value = new WebSocket(wsUrl)

        ws.value.onopen = () => {
            console.log('WebSocket 连接已建立')
        }

        ws.value.onmessage = (event) => {
            console.log('接收到 WebSocket 消息.')

            const resp = JSON.parse(event.data);
            const id = resp.id;

            if (id === 0){  // chatbox 消息
                emitter.emit('message', {'role': "system", 'content': resp.content});
            }
            else if(id === 1){
                emitter.emit('flush_pic', {'base64ImageData': resp.data});
                if(resp.content !== undefined){
                    emitter.emit('message', {'role': "system", 'content': resp.content});
                }
            }

        }

        ws.value.onclose = (event) => {
            console.log('WebSocket 连接已关闭')
        }

        ws.value.onerror = (event) => {
            console.log('WebSocket 连接错误')
        }
    }

    const closeWebSocket = () => {
        if (ws.value) {
            ws.value.close()
            ws.value = null
        }
    }

    onMounted(() => {
        initWebSocket()
    })

    onUnmounted(() => {
        closeWebSocket()
    })

    return { ws }
}

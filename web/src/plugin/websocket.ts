import { ref, onMounted, onUnmounted } from 'vue'
import emitter from '../bus'

const wsUrl = 'ws://localhost:9900/ws/'

function sendSystemMessage(content: any){
    emitter.emit('message', {'role': "system", 'content': content});
}

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
            const code = resp.code;
            const content = resp.content;

            const id = resp.id;

            if(code !== 0){  // 处理遇到错误
                sendSystemMessage(content);
                return
            }

            if (id === 0){  // 仅消息
                sendSystemMessage(content);
            }
            else if(id === 1){  // 流线渲染
                emitter.emit('flush_pic', {'base64ImageData': resp.data});
                sendSystemMessage(content);
            }
            else if(id===3){  // 数据集信息
                sendSystemMessage(content);
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

import { ref, onMounted, onUnmounted } from 'vue'

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
            console.log('接收到 WebSocket 消息：', event.data)
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

import axios, { AxiosInstance } from 'axios';

const http: AxiosInstance = axios.create({
    baseURL: 'http://localhost:9900',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});

http.interceptors.request.use(
    (config) => {
        // 在请求发送之前做些什么
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
);

http.interceptors.response.use(
    (response) => {
        // 对响应数据做点什么
        return response.data;
    },
    (error) => {
        // 对响应错误做点什么
        return Promise.reject(error);
    }
);

export default http;


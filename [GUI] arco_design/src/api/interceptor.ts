import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import { Message, Modal } from '@arco-design/web-vue';
import { useUserStore } from '@/store';
import { getToken } from '@/utils/auth';

export interface HttpResponse<T = unknown> {
  status: number;
  msg: string;
  code: number;
  data: T;
}

if (import.meta.env.VITE_API_BASE_URL) {
  axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;
}

axios.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // let each request carry token
    // this example using the JWT token
    // Authorization is a custom headers key
    // please modify it according to the actual situation
    const token = getToken();
    if (token) {
      if (!config.headers) {
        config.headers = {};
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // do something
    return Promise.reject(error);
  }
);
// add response interceptors
axios.interceptors.response.use(
  (response: AxiosResponse<HttpResponse | Blob>) => {
    // 检查请求的responseType，如果是下载文件，则直接返回响应
    if (response.config.responseType === 'blob' || response.config.responseType === 'arraybuffer') {
      return response;
    }

    // 处理 JSON 响应
    const res = response.data;
    if (typeof res === 'object' && res.code === 0) {
      return res; // 返回整个响应体，如果您只需要数据部分，则返回 res.data
    } 
      const message = res.message || 'Error';
      Message.error({
        content: message,
        duration: 5000,
      });
      return Promise.reject(new Error(message));
    
  },
  (error) => {
    // 从响应中提取错误信息，适应不同错误结构
    const errorMessage = error.response?.data?.message || error.message || 'Request Error';
    Message.error({
      content: errorMessage,
      duration: 5000,
    });
    return Promise.reject(error);
  }
);

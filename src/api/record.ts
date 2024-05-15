import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';

export interface AttackRecord {
  id: number;
  uuid: string;
  domain: string;
  url: string;
  proto: string;
  header: string;
  body: string;
  remoteAddr: string;
  rule_name: string;
  rule_desc: string;
  datetime: string;
}

export interface AttackParams extends Partial<AttackRecord> {
  current: number;
  pageSize: number;
}

export interface AttackListRes {
  data: AttackRecord[];
  current: number;
  pageSize: number;
  total: number;
}

export function queryAttackList(params: AttackParams) {
  return axios.get<AttackListRes>('/api/data/attack/record', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export interface ActionLogRecord {
  id: number;
  type: string;
  location: string;
  message: string;
  user: string;
  datetime: string;
}

export interface ActionLogParams extends Partial<ActionLogRecord> {
  current: number;
  pageSize: number;
}

export interface ActionLogListRes {
  data: ActionLogRecord[];
  current: number;
  pageSize: number;
  total: number;
}

export function queryActionLogkList(params: ActionLogParams) {
  return axios.get<ActionLogListRes>('/api/data/log/action/', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}


export interface LoginLogRecord {
  id: number;
  user: string;
  status: string;
  login_ip: string;
  login_time: string;
}

export interface LoginLogParams extends Partial<LoginLogRecord> {
  current: number;
  pageSize: number;
}

export interface LoginLogListRes {
  data: LoginLogRecord[];
  current: number;
  pageSize: number;
  total: number;
}

export function queryLoginLogList(params: LoginLogParams) {
  return axios.get<LoginLogListRes>('/api/data/log/login/', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export function downloadAttackList() {
  return axios.get('/api/data/log/attack/download', {
    responseType: 'blob', // 指定响应类型为blob
  });
}

export function downloadLoginLogList() {
  return axios.get('/api/data/log/login/download', {
    responseType: 'blob', // 指定响应类型为blob
  });
}

export function downloadActionLogList() {
  return axios.get<AttackListRes>('/api/data/log/action/download', {
    responseType: 'blob', // 指定响应类型为blob
  });
}

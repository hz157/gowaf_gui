import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';

export interface RuleRecord {
  id: string;
  status: 'valid' | 'invalid';
  rule_name: string;
  desc: string;
  reg: string;
  datetime: number;
}

export interface RuleParams extends Partial<RuleRecord> {
  current: number;
  pageSize: number;
}

export interface RuleListRes {
  data: RuleRecord[];
  current: number;
  pageSize: number;
  total: number;
}

export function queryRuleList(params: RuleParams) {
  return axios.get<RuleListRes>('/api/rule/get', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

export interface SwitchRes {
  code: number;
  message: string;
  data: string;
  datetime: string;
}

export interface SwitchData {
  rule_id: number;
}

export function switchRuleStatus(data: SwitchData) {
  return axios.post<SwitchRes>('/api/rule/switch', data);
}

export interface AddRuleStr {
  name: string;
  desc: string;
  reg: string;
  field: string;
}

export interface AddRuleRes {
  rule_id: number;
}

export function AddRule(data: AddRuleStr) {
  return axios.post<AddRuleRes>('/api/rule/add', data);
}

export function Download() {
  return axios.get('/api/rule/download', {
    responseType: 'blob', // 指定响应类型为blob
  });
}

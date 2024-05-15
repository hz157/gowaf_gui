import axios from 'axios';
import type { TableData } from '@arco-design/web-vue/es/table/interface';

export interface ContentDataRecord {
  x: string;
  y: number;
}


export function queryContentData() {
  return axios.get<ContentDataRecord[]>('/api/content-data');
}

export interface NetworkSpeed {
  sent: number;
  recv: number;
}

export interface SystemStatus {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_speed: NetworkSpeed;
}

export function querySystemStatus() {
  return axios.get<SystemStatus>('/api/data/status/sys');
}

export interface CountryData {
  name: string;
  value: number;
}

interface MapData {
  data: CountryData[];
}

export function queryWorldRequest() {
  return axios.get<MapData>('/api/data/request/map');
}


export interface AttackType {
  name: string;
  value: number;
}

interface AttackTypeData {
  data: AttackType[];
}

export function queryAttackType() {
  return axios.get<AttackTypeData>('/api/data/attack/type');
}

interface QPS {
  QPS: number;
}

export function queryQPS() {
  return axios.get<QPS>('/api/data/request/qps');
}

export interface PopularRecord {
  key: number;
  clickNumber: string;
  title: string;
  increases: number;
}

export function queryPopularList(params: { type: string }) {
  return axios.get<TableData[]>('/api/popular/list', { params });
}

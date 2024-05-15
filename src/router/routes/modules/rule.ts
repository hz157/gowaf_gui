/*
 * @Descripttion: 
 * @version: 
 * @Author: Ryan Zhang (gitHub.com/hz157)
 * @Date: 2024-04-25 00:50:47
 * @LastEditors: Ryan Zhang
 * @LastEditTime: 2024-05-15 00:57:33
 */
import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const RULE: AppRouteRecordRaw = {
  path: '/rule',
  name: 'rule',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.rule',
    requiresAuth: true,
    icon: 'icon-settings',
    order: 1,
  },
  children: [
    {
      path: 'manage',
      name: 'Manage',
      component: () => import('@/views/rule/manage/index.vue'),
      meta: {
        locale: 'menu.rule.manage',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'create',
      name: 'Create',
      component: () => import('@/views/rule/create/index.vue'),
      meta: {
        locale: 'menu.rule.create',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true, // 这个属性使得该路由不会显示在导航菜单中
      },
    },
  ],
};

export default RULE;

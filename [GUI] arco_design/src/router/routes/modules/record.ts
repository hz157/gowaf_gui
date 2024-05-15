import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const RECORD: AppRouteRecordRaw = {
    path: '/record',
    name: 'record',
    component: DEFAULT_LAYOUT,
    meta: {
        locale: 'menu.record',
        requiresAuth: true,
        icon: 'icon-bookmark',
        order: 2,
    },
    children: [
        {
            path: 'attack',
            name: 'attack',
            component: () => import('@/views/record/attack/index.vue'),
            meta: {
                locale: 'menu.record.attack',
                requiresAuth: true,
                roles: ['*'],
            },
        },
        {
            path: 'action-log',
            name: 'action-log',
            component: () => import('@/views/record/action-log/index.vue'),
            meta: {
                locale: 'menu.record.action',
                requiresAuth: true,
                roles: ['*'],
            },
        },
        {
            path: 'login-log',
            name: 'login-log',
            component: () => import('@/views/record/login-log/index.vue'),
            meta: {
                locale: 'menu.record.login',
                requiresAuth: true,
                roles: ['*'],
            },
        },
    ],
};
export default RECORD;

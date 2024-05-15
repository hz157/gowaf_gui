import localeMessageBox from '@/components/message-box/locale/zh-CN';
import localeLogin from '@/views/login/locale/zh-CN';

import localeWorkplace from '@/views/dashboard/workplace/locale/zh-CN';
import localeRuleManage from '@/views/rule/manage/locale/zh-CN';
import localeRecordAttack from '@/views/record/attack/locale/zh-CN';
import localeRecordAction from '@/views/record/action-log/locale/zh-CN';
import localeRecordLogin from '@/views/record/login-log/locale/zh-CN';
import localeRuleCreate from '@/views/rule/create/locale/zh-CN';

import localeSettings from './zh-CN/settings';

export default {
  'menu.dashboard': '仪表盘',
  'menu.rule': '规则管理',
  'menu.record': '记录管理',
  'menu.record.attack': '攻击记录',
  'menu.record.action': '操作日志',
  'menu.record.login': '登录日志',
  'menu.server.dashboard': '仪表盘-服务端',
  'menu.server.workplace': '工作台-服务端',
  'menu.server.monitor': '实时监控-服务端',
  'menu.list': '列表页',
  'menu.result': '结果页',
  'menu.exception': '异常页',
  'menu.form': '表单页',
  'menu.profile': '详情页',
  'menu.visualization': '数据可视化',
  'menu.user': '个人中心',
  'menu.arcoWebsite': 'Web应用防火墙(WAF)',
  'menu.faq': '常见问题',
  'navbar.docs': '文档中心',
  'navbar.action.locale': '切换为中文',
  ...localeSettings,
  ...localeMessageBox,
  ...localeLogin,
  ...localeWorkplace,
  ...localeRuleManage,
  ...localeRuleCreate,
  ...localeRecordAttack,
  ...localeRecordAction,
  ...localeRecordLogin,
};

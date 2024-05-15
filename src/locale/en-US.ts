import localeMessageBox from '@/components/message-box/locale/en-US';
import localeLogin from '@/views/login/locale/en-US';

import localeWorkplace from '@/views/dashboard/workplace/locale/en-US';
import localeRuleManage from '@/views/rule/manage/locale/en-US';
import localeRecordAttack from '@/views/record/attack/locale/en-US';
import localeRecordAction from '@/views/record/action-log/locale/en-US';
import localeRecordLogin from '@/views/record/login-log/locale/en-US';
import localeRuleCreate from '@/views/rule/create/locale/en-US';

import localeSettings from './en-US/settings';

export default {
  'menu.dashboard': 'Dashboard',
  'menu.rule': 'Rule Manage',
  'menu.record': 'Record Manage',
  'menu.record.attack': 'Attack Record',
  'menu.record.action': 'Action Logs',
  'menu.record.login': 'Login Logs',
  'menu.server.dashboard': 'Dashboard-Server',
  'menu.server.workplace': 'Workplace-Server',
  'menu.server.monitor': 'Monitor-Server',
  'menu.list': 'List',
  'menu.result': 'Result',
  'menu.exception': 'Exception',
  'menu.form': 'Form',
  'menu.profile': 'Profile',
  'menu.visualization': 'Data Visualization',
  'menu.user': 'User Center',
  'menu.arcoWebsite': 'Web Application Firewall(WAF)',
  'menu.faq': 'FAQ',
  'navbar.docs': 'Docs',
  'navbar.action.locale': 'Switch to English',
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

<template>
  <a-grid :cols="24" :row-gap="16" class="panel">
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 6 }"
    >
      <a-space>
        <a-avatar :size="54" class="col-avatar">
          <img alt="avatar" src="@/assets/images/dashboard/cpu.png" />
        </a-avatar>
        <a-statistic
          :title="$t('workplace.cpu_lable')"
          :value="systemStatus.cpu_usage"
          :precision="1"
          :value-from="0"
          animation
          show-group-separator
        >
          <template #suffix>
            <span class="unit">%</span>
          </template>
        </a-statistic>
      </a-space>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 6 }"
    >
      <a-space>
        <a-avatar :size="54" class="col-avatar">
          <img alt="avatar" src="@/assets/images/dashboard/memory.png" />
        </a-avatar>
        <a-statistic
          :title="$t('workplace.memory_lable')"
          :value="systemStatus.memory_usage"
          :value-from="0"
          animation
          show-group-separator
        >
          <template #suffix>
            <span class="unit">%</span>
          </template>
        </a-statistic>
      </a-space>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 6 }"
    >
      <a-space>
        <a-avatar :size="54" class="col-avatar">
          <img alt="avatar" src="@/assets/images/dashboard/disk.png" />
        </a-avatar>
        <a-statistic
          :title="$t('workplace.disk_lable')"
          :value="systemStatus.disk_usage"
          :value-from="0"
          animation
          show-group-separator
        >
          <template #suffix>
            <span class="unit">%</span>
          </template>
        </a-statistic>
      </a-space>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 6 }"
      style="border-right: none"
    >
      <a-space>
        <a-avatar :size="54" class="col-avatar">
          <img alt="avatar" src="@/assets/images/dashboard/network.png" />
        </a-avatar>
        <a-statistic
          :title="$t('workplace.network_lable.send')"
          :value="systemStatus.network_speed.sent"
          :precision="1"
          :value-from="0"
          animation
        >
          <template #suffix> MB/s </template>
        </a-statistic>
        <a-statistic
          :title="$t('workplace.network_lable.recv')"
          :value="systemStatus.network_speed.recv"
          :precision="1"
          :value-from="0"
          animation
        >
          <template #suffix> MB/s </template>
        </a-statistic>
      </a-space>
    </a-grid-item>
    <a-grid-item :span="24">
      <a-divider class="panel-border" />
    </a-grid-item>
  </a-grid>
</template>

<script lang="ts" setup>
  import { querySystemStatus, SystemStatus } from '@/api/dashboard';
  import useLoading from '@/hooks/loading';
  import { onMounted, onUnmounted, reactive } from 'vue';

  const { loading, setLoading } = useLoading(true);
  const systemStatus = reactive<SystemStatus>({
    cpu_usage: 0,
    memory_usage: 0,
    disk_usage: 0,
    network_speed: { sent: 0, recv: 0 },
  });
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await querySystemStatus();
      systemStatus.cpu_usage = response.data.cpu_usage;
      systemStatus.memory_usage = response.data.memory_usage;
      systemStatus.disk_usage = response.data.disk_usage;
      systemStatus.network_speed.sent = response.data.network_speed.sent;
      systemStatus.network_speed.recv = response.data.network_speed.recv;
    } catch (err) {
      // handle error
    } finally {
      setLoading(false);
    }
  };

  let intervalId: number;

  onMounted(() => {
    fetchData(); // 首次加载即调用
    intervalId = setInterval(fetchData, 5000); // 设置定时器，每5秒调用一次
  });

  onUnmounted(() => {
    clearInterval(intervalId); // 清除定时器
  });
</script>

<style lang="less" scoped>
  .arco-grid.panel {
    margin-bottom: 0;
    padding: 16px 20px 0 20px;
  }
  .panel-col {
    padding-left: 43px;
    border-right: 1px solid rgb(var(--gray-2));
  }
  .col-avatar {
    margin-right: 12px;
    background-color: var(--color-fill-2);
  }
  .up-icon {
    color: rgb(var(--red-6));
  }
  .unit {
    margin-left: 8px;
    color: rgb(var(--gray-8));
    font-size: 12px;
  }
  :deep(.panel-border) {
    margin: 4px 0 0 0;
  }
</style>

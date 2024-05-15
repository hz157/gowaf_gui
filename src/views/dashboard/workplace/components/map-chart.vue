<!--
 * @Descripttion: 
 * @version: 
 * @Author: Ryan Zhang (gitHub.com/hz157)
 * @Date: 2024-04-24 18:55:03
 * @LastEditors: Ryan Zhang
 * @LastEditTime: 2024-04-24 23:31:25
-->
<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      :header-style="{ paddingBottom: 0 }"
      :body-style="{
        paddingTop: '20px',
      }"
      :title="$t('workplace.worldmap_label')"
    >
      <!-- <Chart height="289px" :option="chartOption" /> -->
      <div ref="chartContainer" style="width: 100%; height: 500px"></div>
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import { queryWorldRequest, MapData, } from '@/api/dashboard';
  import world from '@/assets/echarts/geo.json';
  import * as echarts from 'echarts';
  import { useI18n } from 'vue-i18n';
  import { onMounted, onUnmounted, ref, reactive } from 'vue';

  echarts.registerMap('world', JSON.stringify(world));
  const { t } = useI18n();
  const chartContainer = ref(null);
  let myChart: echarts.ECharts|null = null;
  const state = reactive({
    loading: true,
    data: [],
  });
  const fetchData = async () => {
    try {
      const response = await queryWorldRequest();
      state.data = response.data; // 确保响应数据被赋值到响应式状态变量
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      state.loading = false;
    }
  };

  // 初始化图表
  const initChart = () => {
    if (chartContainer.value && !myChart) {
      myChart = echarts.init(chartContainer.value);
      myChart.setOption({
        tooltip: {
          trigger: 'item',
        },
        visualMap: {
          min: 0,
          max: 10000,
          text: ['High', 'Low'],
          realtime: false,
          calculable: true,
          inRange: {
            color: ['#cce5f3', '#99cce6', '#6daed5', '#4191c5', '#2070b4'],
          },
        },
        series: [
          {
            name: t('workplace.worldmap_unit'),
            type: 'map',
            mapType: 'world',
            roam: false,
            data: state.data, // 使用从服务器获取的数据
          },
        ],
      });
    }
  };

  const resizeChart = () => {
    if (myChart) {
      myChart.resize();
    }
  };

  onMounted(async () => {
    await fetchData(); // 在组件挂载时请求数据
    initChart();
    window.addEventListener('resize', resizeChart);
  });

  onUnmounted(() => {
    window.removeEventListener('resize', resizeChart);
    if (myChart != null) {
      myChart.dispose();
    }
  });
  fetchData();
</script>

<style scoped lang="less"></style>

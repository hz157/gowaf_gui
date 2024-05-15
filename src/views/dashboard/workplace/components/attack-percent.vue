<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-card
      class="general-card"
      :header-style="{ paddingBottom: '0' }"
      :body-style="{
        padding: '20px',
      }"
    >
      <template #title>
        {{ $t('workplace.attackPercent_label') }}
      </template>
      <div ref="chartContainer" class="chart-container"></div>
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import { onMounted, ref, onUnmounted, nextTick } from 'vue';
  import * as echarts from 'echarts';
  import useLoading from '@/hooks/loading';
  import { queryAttackType } from '@/api/dashboard';
  import axios from 'axios';

  const { loading, setLoading } = useLoading();
  const chartContainer = ref(null);
  let myChart = null;
  const data = ref([]);

  const bluePalette = [
    '#346751', '#C84B31', '#ECDBBA', '#2F86A6',
    '#402E2A', '#D8B4A0', '#A2B5BB', '#0F4C5C'
  ];

  const initChart = () => {
    if (chartContainer.value && !myChart) {
      myChart = echarts.init(chartContainer.value);
    }
  };

  const fetchDataAndSetChart = async (attempt = 0) => {
    setLoading(true);
    try {
      const response = queryAttackType();
      console.log(response);
      data.value = (await response).data.filter(
        (item) => item.name !== 'TOTAL'
      );
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: data.value.map(item => item.name),
          textStyle: { color: '#003f5c' }
        },
        series: [
          {
            name: 'Attack Types',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: data.value.map((item, index) => ({
              value: item.value,
              name: item.name,
              itemStyle: { color: bluePalette[index % bluePalette.length] }
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
        }]
      };
      myChart.setOption(option);
    } catch (error) {
      console.error('Failed to fetch data:', error);
      if (attempt < 5) {
        console.log(`Retry attempt ${attempt + 1}`);
        await fetchDataAndSetChart(attempt + 1);
      } else {
        console.error('Maximum retry attempts reached. Stopping retries.');
      }
    } finally {
      setLoading(false);
    }
  };

  const resizeChart = () => {
    if (myChart) {
      myChart.resize();
    }
  };

  onMounted(() => {
    requestAnimationFrame(() => {
      initChart();
      fetchDataAndSetChart();
    });
    window.addEventListener('resize', resizeChart);
  });

  onUnmounted(() => {
    if (myChart) {
      myChart.dispose();
    }
  });
</script>

<style scoped lang="less">
  .chart-container {
    height: 300px; // 确保有足够的高度
    width: 100%; // 宽度设置为 100%
  }
</style>

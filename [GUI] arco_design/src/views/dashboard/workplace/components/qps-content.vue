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
        {{ $t('workplace.qps_label') }}
      </template>
      <div ref="chartContainer" class="chart-container"></div>
    </a-card>
  </a-spin>
</template>

<script lang="ts" setup>
  import { onMounted, ref, onUnmounted, watch } from 'vue';
  import * as echarts from 'echarts';
  import useLoading from '@/hooks/loading';
  import { queryQPS } from '@/api/dashboard';

  const { loading, setLoading } = useLoading();
  const chartContainer = ref<HTMLElement | null>(null);
  let myChart: echarts.ECharts | null = null;
  const data = ref<number[]>([]);

  // Initialize ECharts instance
  const initChart = () => {
    if (chartContainer.value && !myChart) {
      // Delay initialization to ensure container size has been calculated
      setTimeout(() => {
        myChart = echarts.init(chartContainer.value);
        // Resize chart when window size changes
        window.addEventListener('resize', () => {
          if (myChart) {
            myChart.resize();
          }
        });
      }, 100);
    }
  };

  // Update the chart with the latest data
  const updateChart = () => {
    if (myChart) {
      myChart.setOption({
        xAxis: {
          type: 'category',
          data: Array.from({ length: data.value.length }, (_, i) => {
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            return `${hours}:${minutes}:${seconds}`;
          }), // X-axis labels with current time (hours:minutes:seconds)
        },
        yAxis: {
          type: 'value',
        },
        tooltip: {
          trigger: 'axis', // Show tooltip when hovering over axis
          formatter: '{b}: {c}', // Display time and value in tooltip
        },
        series: [
          {
            data: data.value,
            type: 'line',
          },
        ],
      });
    }
  };

  // Fetch data and update chart
  const fetchDataAndSetChart = async () => {
    setLoading(true);
    try {
      const response = await queryQPS();
      const newDataPoint = response.data.QPS;

      // Add the new data point to the data array
      data.value.push(newDataPoint);

      // Keep only the latest 10 data points
      if (data.value.length > 10) {
        data.value.shift(); // Remove the oldest data point
      }

      // Update the chart
      updateChart();
    } catch (error) {
      console.error('Failed to fetch QPS data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch data and update chart on component mount
  onMounted(() => {
    initChart();
    fetchDataAndSetChart();
  });

  // Fetch data and update chart every 10 seconds
  const timer = setInterval(fetchDataAndSetChart, 10000);

  // Ensure chart updates when container size changes
  watch(chartContainer, () => {
    if (myChart) {
      myChart.resize();
    }
  });

  // Clear interval on component unmount
  onUnmounted(() => {
    clearInterval(timer);
  });
  </script>

  <style scoped lang="less">
  .chart-container {
    height: 300px; // Ensure sufficient height
    width: 100%; // Set width to 100%
  }
</style>

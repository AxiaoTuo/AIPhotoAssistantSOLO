<template>
  <div class="radar-container" ref="chartRef"></div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  scores: {
    type: Object,
    required: true,
    default: () => ({
      technical: 0,
      composition: 0,
      aesthetic: 0,
      narrative: 0
    })
  }
})

const chartRef = ref(null)
let chart = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  
  // 配置选项
  const option = {
    backgroundColor: 'transparent',
    radar: {
      indicator: [
        { name: '技术', max: 100 },
        { name: '构图', max: 100 },
        { name: '美学', max: 100 },
        { name: '叙事', max: 100 }
      ],
      radius: '70%',
      splitNumber: 4,
      axisName: {
        color: '#333',
        fontSize: 12
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(255, 255, 255, 0.5)', 'rgba(200, 200, 200, 0.5)']
        }
      },
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      },
      splitLine: {
        lineStyle: {
          color: '#ccc'
        }
      }
    },
    series: [
      {
        name: '评分',
        type: 'radar',
        data: [
          {
            value: [
              props.scores.technical,
              props.scores.composition,
              props.scores.aesthetic,
              props.scores.narrative
            ],
            name: '当前评分',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.3)'
            },
            lineStyle: {
              color: '#409eff'
            },
            itemStyle: {
              color: '#409eff'
            }
          }
        ]
      }
    ]
  }
  
  chart.setOption(option)
}

// 响应窗口大小变化
const handleResize = () => {
  chart?.resize()
}

// 监听数据变化
watch(
  () => props.scores,
  () => {
    if (chart) {
      chart.setOption({
        series: [
          {
            data: [
              {
                value: [
                  props.scores.technical,
                  props.scores.composition,
                  props.scores.aesthetic,
                  props.scores.narrative
                ]
              }
            ]
          }
        ]
      })
    }
  },
  { deep: true }
)

onMounted(() => {
  nextTick(() => {
    initChart()
    window.addEventListener('resize', handleResize)
  })
})
</script>

<style scoped>
.radar-container {
  width: 100%;
  height: 300px;
}
</style>
import { CommonModule } from '@angular/common';
import { Component, Input, input, InputSignal } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';
import { EChartsOption, SeriesOption } from 'echarts';
import { NgxEchartsDirective, provideEcharts } from 'ngx-echarts';

@Component({
  selector: 'app-chart',
  imports: [CommonModule, NgxEchartsDirective],
  templateUrl: './chart.component.html',
  styleUrl: './chart.component.scss',
  providers: [
    provideEcharts(),
  ],
})

export class ChartComponent {
  isLoading = true;
  options: EChartsOption = {};
  xAxisData = input<any[]>([]);
  yAxisSeries = input<any>(null);
  chartType = input<
    'line' | 'bar'
  >('line');
  
  constructor() {
    toObservable(this.yAxisSeries).subscribe((data) => {
      if (data) {
        this.initChart();
      }
    });

    this.isLoading = false;
    
    toObservable(this.chartType).subscribe((type) => {
      if (type) {
        this.initChart();
      }
    });
  }

  initChart(): void {
    const xAxis = this.xAxisData();
    const data = this.yAxisSeries();
    const series: any[] = [];
    Object.entries(data).forEach(([name, data]) => {
      series.push({
        name,
        type: this.chartType(),
        data,
        animatedelay: (idx: number) => idx * 10,
      });
    });

    this.options = {
      dataZoom: [
        {
          id: 'dataZoomX',
          type: 'slider',
          filterMode: 'filter',
          xAxisIndex: [0],
        },
        {
          id: 'dataZoomY',
          type: 'slider',
          filterMode: 'empty',
          yAxisIndex: [0],
        }
      ],
      legend : {
        data: Object.keys(data),
        align: 'left', 
      },
      tooltip: {
        trigger: 'axis',
      },
      xAxis: {
        type: 'category',
        data: xAxis,
        axisLabel: {
          rotate: 30,
        },
      },
      yAxis: {
        type: 'value',
      },
      series: series,
    };
  }
}

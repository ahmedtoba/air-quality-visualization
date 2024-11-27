import { Component, DestroyRef, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ChartComponent } from "../../components/chart/chart.component";
import { CommonModule } from '@angular/common';
import { AirQualityData } from '../../models/air-quality-data.model';
import { DataServiceService } from '../../services/data-service.service';
import { provideNativeDateAdapter } from '@angular/material/core';

@Component({
  selector: 'app-dashboard',
  imports: [
    ReactiveFormsModule, 
    ChartComponent, 
    CommonModule, 
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  providers: [
    provideNativeDateAdapter(),
  ],
})
export class DashboardComponent {
  parameters = ['CO_GT', 'PT08_S1_CO', 'NMHC_GT', 'C6H6_GT', 'PT08_S2_NMHC', 'NOX_GT', 'PT08_S3_NOx', 'NO2_GT', 'PT08_S4_NO2', 'PT08_S5_O3', 'T', 'RH', 'AH'];
  xAxisData = signal<any[]>([]);
  yAxisSeries = signal<any>({});
  chartType = signal<'line' | 'bar'>('line');

  destroyRef = inject(DestroyRef);

  dataService = inject(DataServiceService);
  
  public chartTypeButtonGroup: FormGroup;

  public dataFilters: FormGroup;

  constructor() {
    this.dataFilters = new FormGroup({
      startDate: new FormControl('', Validators.required),
      endDate: new FormControl('', Validators.required),
      parameters: new FormControl([]),
    });

    this.chartTypeButtonGroup = new FormGroup({
      chartType: new FormControl('line'),
    });
  }

  ngOnInit(): void {
    this.initFilters();
    this.dataService.dataChanged.subscribe((data) => {
      this.upadteAxisData(data);
    });
    this.getData();
    this.destroyRef.onDestroy(() => {
      this.dataService.dataChanged.unsubscribe();
    });
  }

  upadteAxisData(data: AirQualityData[]): void {
    if (!data.length) return;

    const xAxis = data.map((d) => d.timestamp);
    const yAxis : {
      [key: string]: any[];
    } = {};
    const parameters = Object.keys(data[0]).filter((key) => key !== 'timestamp');
    parameters.forEach((param) => {
      // @ts-ignore
      yAxis[param] = data.map((d) => d[param]);
    });

    this.xAxisData.set(xAxis);
    this.yAxisSeries.set(yAxis);
  }

  initFilters(): void {
    this.dataFilters.patchValue({
      startDate: new Date('2004-03-10').toString(),
      endDate: new Date('2004-03-15').toString(),
    });
  }

  setChartType(value: 'line' | 'bar'): void {
    this.chartType.set(value);
  }

  getData(): void {
    const { startDate, endDate, parameters } = this.filters;
    if (parameters && parameters.length) {
      this.dataService.get_by_parameter(parameters, startDate, endDate);
    } else {
      this.dataService.get_by_date_range(startDate, endDate);
    }
  }

  get filters() {
    return this.dataFilters.value;
  }
}

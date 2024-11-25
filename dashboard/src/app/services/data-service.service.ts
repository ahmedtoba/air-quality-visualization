import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { environment } from '../../environments/environments';
import { BehaviorSubject, Observable } from 'rxjs';

import { AirQualityData } from '../models/air-quality-data.model';
import { AirQualityDataByParamter } from '../models/air-quality-data-by-paramter.model';
import { DatePipe } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class DataServiceService {
  httpClient = inject(HttpClient);
  baseUrl = environment.apiUrl;
  // data = signal<AirQualityData[] | AirQualityDataByParamter[]>([]);
  dataChanged = new BehaviorSubject<AirQualityData[] | AirQualityDataByParamter[]>([]);
  constructor() { }

  get_by_date_range(start_date: string, end_date: string) : void{
    start_date = this.formatDate(start_date);
    end_date = this.formatDate(end_date);
    this.httpClient.get<any>(`${this.baseUrl}?start_date=${start_date}&end_date=${end_date}`)
    .subscribe((data) => {
      this.dataChanged.next(data);
    });
  }

  get_by_parameter(parameter: string, start_date: string, end_date: string) : void{ 
    start_date = this.formatDate(start_date);
    end_date = this.formatDate(end_date);
    this.httpClient.get<AirQualityDataByParamter[]>(`${this.baseUrl}/${parameter}?start_date=${start_date}&end_date=${end_date}`)
    .subscribe((data) => {
      this.dataChanged.next(data);
    });
  }

  private formatDate(date: string): string {
    return new DatePipe('en-US').transform(date, 'dd-MM-yyyy') || ''
  }
}

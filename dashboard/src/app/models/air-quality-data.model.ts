export interface AirQualityData {
    timestamp: Date;
    CO_GT?: number;
    PT08_S1_CO?: number;
    NMHC_GT?: number;
    C6H6_GT?: number;
    PT08_S2_NMHC?: number;
    NOx_GT?: number;
    PT08_S3_NOx?: number;
    NO2_GT?: number;
    PT08_S4_NO2?: number;
    PT08_S5_O3?: number;
    T?: number;
    RH?: number;
    AH?: number;
}
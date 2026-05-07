import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { SettingsService } from './settings.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
    private settings: SettingsService
  ) { }

  public get(endpoint: string) {
    const url = this.settings.API_URL + endpoint;
    return this.http.get(url);
  }

  public post(endpoint: string, data: any) {
    const url = this.settings.API_URL + endpoint;

    const body = new URLSearchParams();

    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        body.set(key, data[key]);
      }
    });

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post(url, body.toString(), { headers: headers });
  }
}
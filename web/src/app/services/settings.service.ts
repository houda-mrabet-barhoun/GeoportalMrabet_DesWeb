import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {

  public API_URL: string = 'http://localhost:8001/';

  constructor() { }
}
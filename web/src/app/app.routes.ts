import { Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { HelpComponent } from './components/help/help.component';
import { MapComponent } from './components/map/map.component';
import { RutasFormComponent } from './components/forms/rutas-form/rutas-form.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', component: HomeComponent },
  { path: 'help', component: HelpComponent },
  { path: 'map', component: MapComponent },
  { path: 'rutas-form', component: RutasFormComponent },
];
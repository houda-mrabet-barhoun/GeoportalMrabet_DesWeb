import { Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { HelpComponent } from './components/help/help.component';
import { MapComponent } from './components/map/map.component';
import { AboutComponent } from './components/about/about.component';

import { RutasFormComponent } from './components/forms/rutas-form/rutas-form.component';
import { ClientesFormComponent } from './components/forms/clientes-form/clientes-form.component';
import { BarriosFormComponent } from './components/forms/barrios-form/barrios-form.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', component: HomeComponent },
  { path: 'help', component: HelpComponent },
  { path: 'map', component: MapComponent },
  { path: 'about', component: AboutComponent },

  { path: 'rutas-form', component: RutasFormComponent },
  { path: 'clientes-form', component: ClientesFormComponent },
  { path: 'barrios-form', component: BarriosFormComponent },
];
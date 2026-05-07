import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

import { ApiService } from '../../../services/api.service';
import { ServerAnswerModel } from '../../../models/server-answer.model';
import { RutaModel } from '../../../models/ruta.model';

@Component({
  selector: 'app-rutas-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './rutas-form.component.html',
  styleUrl: './rutas-form.component.scss'
})
export class RutasFormComponent {

  public rutasForm: FormGroup;
  public message: string = '';
  public rutas: RutaModel[] = [];

  private baseEndpoint: string = 'geoportal_p1/rutas_view/';

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.rutasForm = this.fb.group({
      id: [''],
      distancia: ['', Validators.required],
      tiempo: ['', Validators.required],
      estado: ['', Validators.required],
      barrio_destino: ['', Validators.required],
      numero_paradas: ['', Validators.required],
      geom: ['', Validators.required]
    });
  }

  public insert(): void {
    const data = this.rutasForm.value;

    this.apiService.post(this.baseEndpoint + 'insert/', data).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const id = serverAnswer.data[0].id;
          this.rutasForm.patchValue({ id: id });
          this.message = 'Ruta inserted. id: ' + id;
        } else {
          this.message = 'Error: ' + serverAnswer.message;
        }
      },
      error: (error: any) => {
        this.message = 'HTTP error: ' + error.message;
      }
    });
  }

  public selectone(): void {
    const id = this.rutasForm.value.id;

    if (!id) {
      this.message = 'You must write an id to select one route';
      return;
    }

    this.apiService.get(this.baseEndpoint + 'selectone/' + id + '/').subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok && serverAnswer.data.length > 0) {
          const ruta = serverAnswer.data[0] as RutaModel;

          this.rutasForm.patchValue({
            id: ruta.id,
            distancia: ruta.distancia,
            tiempo: ruta.tiempo,
            estado: ruta.estado,
            barrio_destino: ruta.barrio_destino,
            numero_paradas: ruta.numero_paradas,
            geom: ruta.geom
          });

          this.rutas = [ruta];
          this.message = 'Ruta retrieved. id: ' + ruta.id;
        } else {
          this.message = 'Error: ' + serverAnswer.message;
        }
      },
      error: (error: any) => {
        this.message = 'HTTP error: ' + error.message;
      }
    });
  }

  public selectall(): void {
    this.apiService.get(this.baseEndpoint + 'selectall/').subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          this.rutas = serverAnswer.data as RutaModel[];
          this.message = 'Rutas retrieved: ' + this.rutas.length;
        } else {
          this.message = 'Error: ' + serverAnswer.message;
        }
      },
      error: (error: any) => {
        this.message = 'HTTP error: ' + error.message;
      }
    });
  }

  public update(): void {
    const id = this.rutasForm.value.id;

    if (!id) {
      this.message = 'You must write an id to update a route';
      return;
    }

    const data = this.rutasForm.value;

    this.apiService.post(this.baseEndpoint + 'update/' + id + '/', data).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const rowsUpdated = serverAnswer.data[0].rows_updated;
          this.message = 'Ruta updated. rows_updated: ' + rowsUpdated;
        } else {
          this.message = 'Error: ' + serverAnswer.message;
        }
      },
      error: (error: any) => {
        this.message = 'HTTP error: ' + error.message;
      }
    });
  }

  public delete(): void {
    const id = this.rutasForm.value.id;

    if (!id) {
      this.message = 'You must write an id to delete a route';
      return;
    }

    this.apiService.post(this.baseEndpoint + 'delete/' + id + '/', {}).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const rowsDeleted = serverAnswer.data[0].rows_deleted;
          this.message = 'Ruta deleted. rows_deleted: ' + rowsDeleted;
          this.clean();
        } else {
          this.message = 'Error: ' + serverAnswer.message;
        }
      },
      error: (error: any) => {
        this.message = 'HTTP error: ' + error.message;
      }
    });
  }

  public clean(): void {
    this.rutasForm.reset();
    this.rutas = [];
  }
}
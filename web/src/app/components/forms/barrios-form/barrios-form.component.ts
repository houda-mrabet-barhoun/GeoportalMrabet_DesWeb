import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

import { ApiService } from '../../../services/api.service';
import { ServerAnswerModel } from '../../../models/server-answer.model';
import { BarrioModel } from '../../../models/barrio.model';

@Component({
  selector: 'app-barrios-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './barrios-form.component.html',
  styleUrl: './barrios-form.component.scss'
})
export class BarriosFormComponent {

  public barriosForm: FormGroup;
  public message: string = '';
  public barrios: BarrioModel[] = [];

  private baseEndpoint: string = 'geoportal_p1/barrios_view/';

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.barriosForm = this.fb.group({
      id: [''],
      nombre: ['', Validators.required],
      codigo: ['', Validators.required],
      distrito: ['', Validators.required],
      area: ['', Validators.required],
      numero_clientes: ['', Validators.required],
      geom: ['', Validators.required]
    });
  }

  public insert(): void {
    const data = this.barriosForm.value;

    this.apiService.post(this.baseEndpoint + 'insert/', data).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const id = serverAnswer.data[0].id;
          this.barriosForm.patchValue({ id: id });
          this.message = 'Barrio inserted. id: ' + id;
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
    const id = this.barriosForm.value.id;

    if (!id) {
      this.message = 'You must write an id to select one barrio';
      return;
    }

    this.apiService.get(this.baseEndpoint + 'selectone/' + id + '/').subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok && serverAnswer.data.length > 0) {
          const barrio = serverAnswer.data[0] as BarrioModel;

          this.barriosForm.patchValue({
            id: barrio.id,
            nombre: barrio.nombre,
            codigo: barrio.codigo,
            distrito: barrio.distrito,
            area: barrio.area,
            numero_clientes: barrio.numero_clientes,
            geom: barrio.geom
          });

          this.barrios = [barrio];
          this.message = 'Barrio retrieved. id: ' + barrio.id;
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
          this.barrios = serverAnswer.data as BarrioModel[];
          this.message = 'Barrios retrieved: ' + this.barrios.length;
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
    const id = this.barriosForm.value.id;

    if (!id) {
      this.message = 'You must write an id to update a barrio';
      return;
    }

    const data = this.barriosForm.value;

    this.apiService.post(this.baseEndpoint + 'update/' + id + '/', data).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const rowsUpdated = serverAnswer.data[0].rows_updated;
          this.message = 'Barrio updated. rows_updated: ' + rowsUpdated;
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
    const id = this.barriosForm.value.id;

    if (!id) {
      this.message = 'You must write an id to delete a barrio';
      return;
    }

    this.apiService.post(this.baseEndpoint + 'delete/' + id + '/', {}).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const rowsDeleted = serverAnswer.data[0].rows_deleted;
          this.message = 'Barrio deleted. rows_deleted: ' + rowsDeleted;
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
    this.barriosForm.reset();
    this.barrios = [];
  }
}
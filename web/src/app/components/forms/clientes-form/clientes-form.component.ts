import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

import { ApiService } from '../../../services/api.service';
import { ServerAnswerModel } from '../../../models/server-answer.model';
import { ClienteModel } from '../../../models/cliente.model';

@Component({
  selector: 'app-clientes-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './clientes-form.component.html',
  styleUrl: './clientes-form.component.scss'
})
export class ClientesFormComponent {

  public clientesForm: FormGroup;
  public message: string = '';
  public clientes: ClienteModel[] = [];

  private baseEndpoint: string = 'geoportal_p1/clientes_view/';

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.clientesForm = this.fb.group({
      id: [''],
      nombre: ['', Validators.required],
      direccion: ['', Validators.required],
      telefono: ['', Validators.required],
      tipo_cliente: ['', Validators.required],
      barrio: ['', Validators.required],
      geom: ['', Validators.required]
    });
  }

  public insert(): void {
    const data = this.clientesForm.value;

    this.apiService.post(this.baseEndpoint + 'insert/', data).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const id = serverAnswer.data[0].id;
          this.clientesForm.patchValue({ id: id });
          this.message = 'Cliente inserted. id: ' + id;
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
    const id = this.clientesForm.value.id;

    if (!id) {
      this.message = 'You must write an id to select one cliente';
      return;
    }

    this.apiService.get(this.baseEndpoint + 'selectone/' + id + '/').subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok && serverAnswer.data.length > 0) {
          const cliente = serverAnswer.data[0] as ClienteModel;

          this.clientesForm.patchValue({
            id: cliente.id,
            nombre: cliente.nombre,
            direccion: cliente.direccion,
            telefono: cliente.telefono,
            tipo_cliente: cliente.tipo_cliente,
            barrio: cliente.barrio,
            geom: cliente.geom
          });

          this.clientes = [cliente];
          this.message = 'Cliente retrieved. id: ' + cliente.id;
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
          this.clientes = serverAnswer.data as ClienteModel[];
          this.message = 'Clientes retrieved: ' + this.clientes.length;
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
    const id = this.clientesForm.value.id;

    if (!id) {
      this.message = 'You must write an id to update a cliente';
      return;
    }

    const data = this.clientesForm.value;

    this.apiService.post(this.baseEndpoint + 'update/' + id + '/', data).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const rowsUpdated = serverAnswer.data[0].rows_updated;
          this.message = 'Cliente updated. rows_updated: ' + rowsUpdated;
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
    const id = this.clientesForm.value.id;

    if (!id) {
      this.message = 'You must write an id to delete a cliente';
      return;
    }

    this.apiService.post(this.baseEndpoint + 'delete/' + id + '/', {}).subscribe({
      next: (response: any) => {
        const serverAnswer = response as ServerAnswerModel;

        if (serverAnswer.ok) {
          const rowsDeleted = serverAnswer.data[0].rows_deleted;
          this.message = 'Cliente deleted. rows_deleted: ' + rowsDeleted;
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
    this.clientesForm.reset();
    this.clientes = [];
  }
}
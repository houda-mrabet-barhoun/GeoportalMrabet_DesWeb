export interface RutaModel {
  id?: number;
  distancia: number;
  tiempo: number;
  estado: string;
  barrio_destino: string;
  numero_paradas: number;
  geom: string;
}
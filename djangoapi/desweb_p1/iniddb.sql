CREATE DATABASE desweb_p1;

CREATE EXTENSION postgis;

CREATE SCHEMA d;

CREATE TABLE d.clientes (
    id serial PRIMARY KEY,
    nombre text,
    direccion text,
    telefono text,
    tipo_cliente text,
    barrio text,
    geom geometry(Point,25830)
);

CREATE TABLE d.barrios (
    id serial PRIMARY KEY,
    nombre text,
    codigo text,
    distrito text,
    geom geometry(Polygon,25830),
    area double precision,
    numero_clientes integer
);

CREATE TABLE d.rutas (
    id serial PRIMARY KEY,
    geom geometry(LineString,25830),
    distancia double precision,
    tiempo integer,
    estado text,
    barrio_destino text,
    numero_paradas integer
);

from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry, LineString
from geoportal_p1.models import Ruta


class RutasDjango:

    def insert(self, d):
        try:
            geom = GEOSGeometry(d["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            if geom.geom_type != "LineString":
                return {
                    "ok": False,
                    "message": "La geometría debe ser de tipo LINESTRING",
                    "data": None
                }

            coords = []
            for x, y in geom.coords:
                coords.append((round(x, 4), round(y, 4)))
            geom = LineString(coords, srid=25830)

            rutas = list(Ruta.objects.all())

            for r_aux in rutas:
                if r_aux.geom and r_aux.geom.intersects(geom):
                    return {
                        "ok": False,
                        "message": "La línea intersecta con otras rutas",
                        "data": None
                    }

            r = Ruta()
            r.distancia = d["distancia"]
            r.tiempo = d["tiempo"]
            r.estado = d["estado"]
            r.barrio_destino = d["barrio_destino"]
            r.numero_paradas = d["numero_paradas"]
            r.geom = geom
            r.save()

            return {
                "ok": True,
                "message": "Datos insertados correctamente",
                "data": [{"id": r.id}]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def update(self, d):
        try:
            id = d["id"]
            l = list(Ruta.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"La ruta con id {id} no existe",
                    "data": None
                }

            geom = GEOSGeometry(d["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            if geom.geom_type != "LineString":
                return {
                    "ok": False,
                    "message": "La geometría debe ser de tipo LINESTRING",
                    "data": None
                }

            coords = []
            for x, y in geom.coords:
                coords.append((round(x, 4), round(y, 4)))
            geom = LineString(coords, srid=25830)

            rutas = list(Ruta.objects.exclude(id=id))

            for r_aux in rutas:
                if r_aux.geom and r_aux.geom.intersects(geom):
                    return {
                        "ok": False,
                        "message": "La línea intersecta con otras rutas",
                        "data": None
                    }

            r = l[0]
            r.distancia = d["distancia"]
            r.tiempo = d["tiempo"]
            r.estado = d["estado"]
            r.barrio_destino = d["barrio_destino"]
            r.numero_paradas = d["numero_paradas"]
            r.geom = geom
            r.save()

            return {
                "ok": True,
                "message": "Datos actualizados correctamente",
                "data": [{"rows_updated": 1}]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def delete(self, d):
        try:
            id = d["id"]
            l = list(Ruta.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"La ruta con id {id} no existe",
                    "data": None
                }

            rows_deleted = len(l)
            l[0].delete()

            return {
                "ok": True,
                "message": "Datos eliminados correctamente",
                "data": [{"rows_deleted": rows_deleted}]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def selectAsTuples(self, d):
        try:
            id = d["id"]
            l = list(Ruta.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"La ruta con id {id} no existe",
                    "data": []
                }

            r = l[0]
            tup = (
                r.id,
                r.geom.wkt if r.geom else None,
                r.distancia,
                r.tiempo,
                r.estado,
                r.barrio_destino,
                r.numero_paradas
            )

            return {
                "ok": True,
                "message": "Datos recuperados correctamente",
                "data": [tup]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def selectAsDicts(self, d):
        try:
            id = d["id"]
            l = list(Ruta.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"La ruta con id {id} no existe",
                    "data": []
                }

            r = l[0]
            di = model_to_dict(r)
            di["geom"] = r.geom.wkt if r.geom else None

            return {
                "ok": True,
                "message": "Datos recuperados correctamente",
                "data": [di]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }
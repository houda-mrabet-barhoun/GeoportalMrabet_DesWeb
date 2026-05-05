from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry, Polygon
from geoportal_p1.models import Barrio


class BarriosDjango:

    def insert(self, d):
        try:
            geom = GEOSGeometry(d["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            if geom.geom_type != "Polygon":
                return {
                    "ok": False,
                    "message": "La geometría debe ser de tipo POLYGON",
                    "data": None
                }

            coords = []
            for x, y in geom.coords[0]:
                coords.append((round(x, 4), round(y, 4)))
            geom = Polygon(coords, srid=25830)

            barrios = list(Barrio.objects.all())

            for b in barrios:
                if b.geom and b.geom.relate_pattern(geom, "T********"):
                    return {
                        "ok": False,
                        "message": "El polígono intersecta con otros barrios",
                        "data": None
                    }

            b = Barrio()
            b.nombre = d["nombre"]
            b.codigo = d["codigo"]
            b.distrito = d["distrito"]
            b.area = d["area"]
            b.numero_clientes = d["numero_clientes"]
            b.geom = geom
            b.save()

            return {
                "ok": True,
                "message": "Datos insertados correctamente",
                "data": [{"id": b.id}]
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
            l = list(Barrio.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El barrio con id {id} no existe",
                    "data": None
                }

            geom = GEOSGeometry(d["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            if geom.geom_type != "Polygon":
                return {
                    "ok": False,
                    "message": "La geometría debe ser de tipo POLYGON",
                    "data": None
                }

            coords = []
            for x, y in geom.coords[0]:
                coords.append((round(x, 4), round(y, 4)))
            geom = Polygon(coords, srid=25830)

            barrios = list(Barrio.objects.exclude(id=id))

            for b_aux in barrios:
                if b_aux.geom and b_aux.geom.relate_pattern(geom, "T********"):
                    return {
                        "ok": False,
                        "message": "El polígono intersecta con otros barrios",
                        "data": None
                    }

            b = l[0]
            b.nombre = d["nombre"]
            b.codigo = d["codigo"]
            b.distrito = d["distrito"]
            b.area = d["area"]
            b.numero_clientes = d["numero_clientes"]
            b.geom = geom
            b.save()

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
            l = list(Barrio.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El barrio con id {id} no existe",
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
            l = list(Barrio.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El barrio con id {id} no existe",
                    "data": []
                }

            b = l[0]
            tup = (
                b.id,
                b.nombre,
                b.codigo,
                b.distrito,
                b.geom.wkt if b.geom else None,
                b.area,
                b.numero_clientes
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
            l = list(Barrio.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El barrio con id {id} no existe",
                    "data": []
                }

            b = l[0]
            di = model_to_dict(b)
            di["geom"] = b.geom.wkt if b.geom else None

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
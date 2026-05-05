from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry, Point
from geoportal_p1.models import Cliente, Barrio


class ClientesDjango:

    def insert(self, d):
        try:
            geom = GEOSGeometry(d["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            if geom.geom_type != "Point":
                return {
                    "ok": False,
                    "message": "La geometría debe ser de tipo POINT",
                    "data": None
                }

            geom = Point(round(geom.x, 4), round(geom.y, 4), srid=25830)

            barrios = list(Barrio.objects.all())
            dentro = False

            for b in barrios:
                if b.geom and geom.within(b.geom):
                    dentro = True
                    break

            if not dentro:
                return {
                    "ok": False,
                    "message": "El punto está fuera de cualquier barrio",
                    "data": None
                }

            c = Cliente()
            c.nombre = d["nombre"]
            c.direccion = d["direccion"]
            c.telefono = d["telefono"]
            c.tipo_cliente = d["tipo_cliente"]
            c.barrio = d["barrio"]
            c.geom = geom
            c.save()

            return {
                "ok": True,
                "message": "Datos insertados correctamente",
                "data": [{"id": c.id}]
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
            l = list(Cliente.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El cliente con id {id} no existe",
                    "data": None
                }

            geom = GEOSGeometry(d["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            if geom.geom_type != "Point":
                return {
                    "ok": False,
                    "message": "La geometría debe ser de tipo POINT",
                    "data": None
                }

            geom = Point(round(geom.x, 4), round(geom.y, 4), srid=25830)

            barrios = list(Barrio.objects.all())
            dentro = False

            for b in barrios:
                if b.geom and geom.within(b.geom):
                    dentro = True
                    break

            if not dentro:
                return {
                    "ok": False,
                    "message": "El punto está fuera de cualquier barrio",
                    "data": None
                }

            c = l[0]
            c.nombre = d["nombre"]
            c.direccion = d["direccion"]
            c.telefono = d["telefono"]
            c.tipo_cliente = d["tipo_cliente"]
            c.barrio = d["barrio"]
            c.geom = geom
            c.save()

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
            l = list(Cliente.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El cliente con id {id} no existe",
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
            l = list(Cliente.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El cliente con id {id} no existe",
                    "data": []
                }

            c = l[0]
            tup = (
                c.id,
                c.nombre,
                c.direccion,
                c.telefono,
                c.tipo_cliente,
                c.barrio,
                c.geom.wkt if c.geom else None
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
            l = list(Cliente.objects.filter(id=id))

            if len(l) == 0:
                return {
                    "ok": False,
                    "message": f"El cliente con id {id} no existe",
                    "data": []
                }

            c = l[0]
            di = model_to_dict(c)
            di["geom"] = c.geom.wkt if c.geom else None

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
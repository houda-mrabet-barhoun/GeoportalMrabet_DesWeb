# Django imports
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry

# Teacher base view
from core.myLib.baseDjangoView import BaseDjangoView

# Project models
from geoportal_p1.models import Cliente, Barrio, Ruta


class HelloGeoportalP1(View):
    def get(self, request):
        return JsonResponse({
            "ok": True,
            "message": "Geoportal P1. Hello world",
            "data": [request.GET.dict()]
        })

    def post(self, request):
        return JsonResponse({
            "ok": True,
            "message": "Geoportal P1. Hello world",
            "data": [request.POST.dict()]
        })


def model_to_clean_dict(obj):
    """
    Converts a Django model object into a dictionary.
    Converts geometry to WKT so it can be sent as JSON.
    """
    d = model_to_dict(obj)

    if obj.geom:
        d["geom"] = obj.geom.wkt
    else:
        d["geom"] = None

    return d


# =========================
# CLIENTES
# =========================

class ClientesView(BaseDjangoView):

    def selectone(self, id):
        clientes = list(Cliente.objects.filter(id=id))

        if len(clientes) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Cliente id {id} does not exist",
                "data": []
            })

        d = model_to_clean_dict(clientes[0])

        return JsonResponse({
            "ok": True,
            "message": "Cliente retrieved",
            "data": [d]
        })

    def selectall(self):
        clientes = Cliente.objects.all()
        data = []

        for cliente in clientes:
            data.append(model_to_clean_dict(cliente))

        return JsonResponse({
            "ok": True,
            "message": "Clientes retrieved",
            "data": data
        })

    def insert(self, request):
        d = request.POST.dict()

        try:
            geom = GEOSGeometry(d["geom"], srid=25830)

            cliente = Cliente(
                nombre=d["nombre"],
                direccion=d["direccion"],
                telefono=d["telefono"],
                tipo_cliente=d["tipo_cliente"],
                barrio=d["barrio"],
                geom=geom
            )

            cliente.save()

            return JsonResponse({
                "ok": True,
                "message": "Cliente inserted",
                "data": [{"id": cliente.id}]
            })

        except Exception as e:
            return JsonResponse({
                "ok": False,
                "message": str(e),
                "data": []
            })

    def update(self, request, id):
        d = request.POST.dict()

        clientes = list(Cliente.objects.filter(id=id))

        if len(clientes) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Cliente id {id} does not exist",
                "data": []
            })

        try:
            cliente = clientes[0]

            cliente.nombre = d["nombre"]
            cliente.direccion = d["direccion"]
            cliente.telefono = d["telefono"]
            cliente.tipo_cliente = d["tipo_cliente"]
            cliente.barrio = d["barrio"]

            if "geom" in d and d["geom"] != "":
                cliente.geom = GEOSGeometry(d["geom"], srid=25830)

            cliente.save()

            return JsonResponse({
                "ok": True,
                "message": "Cliente updated",
                "data": [{"rows_updated": 1}]
            })

        except Exception as e:
            return JsonResponse({
                "ok": False,
                "message": str(e),
                "data": []
            })

    def delete(self, id):
        clientes = list(Cliente.objects.filter(id=id))

        if len(clientes) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Cliente id {id} does not exist",
                "data": [{"rows_deleted": 0}]
            })

        clientes[0].delete()

        return JsonResponse({
            "ok": True,
            "message": "Cliente deleted",
            "data": [{"rows_deleted": 1}]
        })


# =========================
# BARRIOS
# =========================

class BarriosView(BaseDjangoView):

    def selectone(self, id):
        barrios = list(Barrio.objects.filter(id=id))

        if len(barrios) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Barrio id {id} does not exist",
                "data": []
            })

        d = model_to_clean_dict(barrios[0])

        return JsonResponse({
            "ok": True,
            "message": "Barrio retrieved",
            "data": [d]
        })

    def selectall(self):
        barrios = Barrio.objects.all()
        data = []

        for barrio in barrios:
            data.append(model_to_clean_dict(barrio))

        return JsonResponse({
            "ok": True,
            "message": "Barrios retrieved",
            "data": data
        })

    def insert(self, request):
        d = request.POST.dict()

        try:
            geom = GEOSGeometry(d["geom"], srid=25830)

            barrio = Barrio(
                nombre=d["nombre"],
                codigo=d["codigo"],
                distrito=d["distrito"],
                area=float(d["area"]),
                numero_clientes=int(d["numero_clientes"]),
                geom=geom
            )

            barrio.save()

            return JsonResponse({
                "ok": True,
                "message": "Barrio inserted",
                "data": [{"id": barrio.id}]
            })

        except Exception as e:
            return JsonResponse({
                "ok": False,
                "message": str(e),
                "data": []
            })

    def update(self, request, id):
        d = request.POST.dict()

        barrios = list(Barrio.objects.filter(id=id))

        if len(barrios) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Barrio id {id} does not exist",
                "data": []
            })

        try:
            barrio = barrios[0]

            barrio.nombre = d["nombre"]
            barrio.codigo = d["codigo"]
            barrio.distrito = d["distrito"]
            barrio.area = float(d["area"])
            barrio.numero_clientes = int(d["numero_clientes"])

            if "geom" in d and d["geom"] != "":
                barrio.geom = GEOSGeometry(d["geom"], srid=25830)

            barrio.save()

            return JsonResponse({
                "ok": True,
                "message": "Barrio updated",
                "data": [{"rows_updated": 1}]
            })

        except Exception as e:
            return JsonResponse({
                "ok": False,
                "message": str(e),
                "data": []
            })

    def delete(self, id):
        barrios = list(Barrio.objects.filter(id=id))

        if len(barrios) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Barrio id {id} does not exist",
                "data": [{"rows_deleted": 0}]
            })

        barrios[0].delete()

        return JsonResponse({
            "ok": True,
            "message": "Barrio deleted",
            "data": [{"rows_deleted": 1}]
        })


# =========================
# RUTAS
# =========================

class RutasView(BaseDjangoView):

    def selectone(self, id):
        rutas = list(Ruta.objects.filter(id=id))

        if len(rutas) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Ruta id {id} does not exist",
                "data": []
            })

        d = model_to_clean_dict(rutas[0])

        return JsonResponse({
            "ok": True,
            "message": "Ruta retrieved",
            "data": [d]
        })

    def selectall(self):
        rutas = Ruta.objects.all()
        data = []

        for ruta in rutas:
            data.append(model_to_clean_dict(ruta))

        return JsonResponse({
            "ok": True,
            "message": "Rutas retrieved",
            "data": data
        })

    def insert(self, request):
        d = request.POST.dict()

        try:
            geom = GEOSGeometry(d["geom"], srid=25830)

            ruta = Ruta(
                distancia=float(d["distancia"]),
                tiempo=int(d["tiempo"]),
                estado=d["estado"],
                barrio_destino=d["barrio_destino"],
                numero_paradas=int(d["numero_paradas"]),
                geom=geom
            )

            ruta.save()

            return JsonResponse({
                "ok": True,
                "message": "Ruta inserted",
                "data": [{"id": ruta.id}]
            })

        except Exception as e:
            return JsonResponse({
                "ok": False,
                "message": str(e),
                "data": []
            })

    def update(self, request, id):
        d = request.POST.dict()

        rutas = list(Ruta.objects.filter(id=id))

        if len(rutas) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Ruta id {id} does not exist",
                "data": []
            })

        try:
            ruta = rutas[0]

            ruta.distancia = float(d["distancia"])
            ruta.tiempo = int(d["tiempo"])
            ruta.estado = d["estado"]
            ruta.barrio_destino = d["barrio_destino"]
            ruta.numero_paradas = int(d["numero_paradas"])

            if "geom" in d and d["geom"] != "":
                ruta.geom = GEOSGeometry(d["geom"], srid=25830)

            ruta.save()

            return JsonResponse({
                "ok": True,
                "message": "Ruta updated",
                "data": [{"rows_updated": 1}]
            })

        except Exception as e:
            return JsonResponse({
                "ok": False,
                "message": str(e),
                "data": []
            })

    def delete(self, id):
        rutas = list(Ruta.objects.filter(id=id))

        if len(rutas) == 0:
            return JsonResponse({
                "ok": False,
                "message": f"Ruta id {id} does not exist",
                "data": [{"rows_deleted": 0}]
            })

        rutas[0].delete()

        return JsonResponse({
            "ok": True,
            "message": "Ruta deleted",
            "data": [{"rows_deleted": 1}]
        })

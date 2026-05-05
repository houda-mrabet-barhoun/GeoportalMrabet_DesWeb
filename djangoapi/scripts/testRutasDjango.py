from scripts.rutasDjango import RutasDjango
#python manage.py runscript testRutasDjango

def run(*args):

    d = {
        "id": 1,
        "geom": "LINESTRING(724500 4369500, 725500 4370500)",
        "distancia": 1500.0,
        "tiempo": 12,
        "estado": "activa",
        "barrio_destino": "Benimaclet",
        "numero_paradas": 3
    }

    r = RutasDjango()

    print("INSERT")
    print(r.insert(d))

    print("UPDATE")
    print(r.update(d))

    print("SELECT AS TUPLES")
    print(r.selectAsTuples(d))

    print("SELECT AS DICTS")
    print(r.selectAsDicts(d))

    print("DELETE")
    print(r.delete(d))
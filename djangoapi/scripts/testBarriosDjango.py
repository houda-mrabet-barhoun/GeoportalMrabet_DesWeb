from scripts.barriosDjango import BarriosDjango
#python manage.py runscript testBarriosDjango

def run(*args):

    d = {
        "id": 1,
        "nombre": "Barrio Django",
        "codigo": "B001",
        "distrito": "Pla del Real",
        "area": 4000000.0,
        "numero_clientes": 0,
        "geom": "POLYGON((724000 4369000, 726000 4369000, 726000 4371000, 724000 4371000, 724000 4369000))"
    }

    b = BarriosDjango()

    print("INSERT")
    print(b.insert(d))

    print("UPDATE")
    print(b.update(d))

    print("SELECT AS TUPLES")
    print(b.selectAsTuples(d))

    print("SELECT AS DICTS")
    print(b.selectAsDicts(d))

    print("DELETE")
    print(b.delete(d))
import json

from scripts.clientesDjango import ClientesDjango
from scripts.barriosDjango import BarriosDjango
from scripts.rutasDjango import RutasDjango


def run(*args):
    if len(args) != 3:
        print("Error: debes pasar 3 parámetros: tabla, función y diccionario_json")
        return

    table_name = args[0]
    function_name = args[1]
    json_data = args[2]

    try:
        d = json.loads(json_data)
    except Exception:
        print("Error: el tercer parámetro debe ser un JSON válido")
        return

    if table_name not in ["clientes", "barrios", "rutas"]:
        print("Error: las tablas disponibles son clientes, barrios y rutas")
        return

    if function_name not in ["insert", "selectAsTuples", "selectAsDicts", "update", "delete"]:
        print("Error: las funciones disponibles son insert, selectAsTuples, selectAsDicts, update y delete")
        return

    if table_name == "clientes":
        obj = ClientesDjango()
    elif table_name == "barrios":
        obj = BarriosDjango()
    else:
        obj = RutasDjango()

    if function_name == "insert":
        r = obj.insert(d)
    elif function_name == "selectAsTuples":
        r = obj.selectAsTuples(d)
    elif function_name == "selectAsDicts":
        r = obj.selectAsDicts(d)
    elif function_name == "update":
        r = obj.update(d)
    elif function_name == "delete":
        r = obj.delete(d)

    print(r)
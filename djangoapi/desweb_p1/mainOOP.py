import sys
import json

from clientes.clientesOOP import ClientesOOP
from barrios.barriosOOP import BarriosOOP
from rutas.rutasOOP import RutasOOP


def main():
    if len(sys.argv) != 4:
        print("Error: debes pasar 3 parámetros: tabla, función y diccionario_json")
        sys.exit(0)

    tableName = sys.argv[1]
    functionName = sys.argv[2]
    jsonData = sys.argv[3]

    try:
        d = json.loads(jsonData)
    except Exception:
        print("Error: el tercer parámetro debe ser un JSON válido")
        sys.exit(0)

    if tableName not in ["clientes", "barrios", "rutas"]:
        print("Error: las tablas disponibles son clientes, barrios y rutas")
        sys.exit(0)

    if functionName not in ["insert", "selectAsTuples", "selectAsDicts", "update", "delete"]:
        print("Error: las funciones disponibles son insert, selectAsTuples, selectAsDicts, update y delete")
        sys.exit(0)

    if tableName == "clientes":
        obj = ClientesOOP()
    elif tableName == "barrios":
        obj = BarriosOOP()
    elif tableName == "rutas":
        obj = RutasOOP()

    if functionName == "insert":
        r = obj.insert(d)
    elif functionName == "selectAsTuples":
        r = obj.selectAsTuples(d)
    elif functionName == "selectAsDicts":
        r = obj.selectAsDicts(d)
    elif functionName == "update":
        r = obj.update(d)
    elif functionName == "delete":
        r = obj.delete(d)

    print(r)


if __name__ == "__main__":
    main()
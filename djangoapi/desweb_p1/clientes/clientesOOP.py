from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class ClientesOOP():

    def __init__(self):
        self.conn = connect()
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self, d):
        try:
            q_valid = """
            SELECT ST_IsValid(
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                )
            )
            """
            self.cur.execute(q_valid, [d["geom"], EPSG_CODE])
            valid_result = self.cur.fetchall()

            if not valid_result or valid_result[0][0] is not True:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            q_within = """
            SELECT id
            FROM d.barrios
            WHERE ST_Within(
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                ),
                geom
            )
            """
            self.cur.execute(q_within, [d["geom"], EPSG_CODE])
            within_result = self.cur.fetchall()

            if len(within_result) == 0:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "El punto está fuera de cualquier barrio",
                    "data": None
                }

            cons = """
            INSERT INTO d.clientes
                (nombre, direccion, telefono, tipo_cliente, barrio, geom)
            VALUES
                (%s, %s, %s, %s, %s,
                 ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                 )
                )
            RETURNING id
            """

            self.cur.execute(cons, [
                d["nombre"],
                d["direccion"],
                d["telefono"],
                d["tipo_cliente"],
                d["barrio"],
                d["geom"],
                EPSG_CODE
            ])

            self.conn.commit()
            l = self.cur.fetchall()

            self.disconnect()

            return {
                "ok": True,
                "message": "Cliente insertado correctamente",
                "data": [{"id": l[0][0]}]
            }

        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def selectAsTuples(self, d):
        try:
            cons = """
            SELECT id, nombre, direccion, telefono, tipo_cliente, barrio, ST_AsText(geom)
            FROM d.clientes
            WHERE id = %s
            """

            self.cur.execute(cons, [d["id"]])
            l = self.cur.fetchall()

            self.disconnect()

            return {
                "ok": True,
                "message": "Datos recuperados correctamente",
                "data": l
            }

        except Exception as e:
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def selectAsDicts(self, d):
        try:
            self.cur.close()
            self.cur = self.conn.cursor(row_factory=dict_row)

            cons = """
            SELECT id, nombre, direccion, telefono, tipo_cliente, barrio, ST_AsText(geom) AS geom
            FROM d.clientes
            WHERE id = %s
            """

            self.cur.execute(cons, [d["id"]])
            l = self.cur.fetchall()

            self.disconnect()

            return {
                "ok": True,
                "message": "Datos recuperados correctamente",
                "data": l
            }

        except Exception as e:
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def update(self, d):
        try:
            q_valid = """
            SELECT ST_IsValid(
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                )
            )
            """
            self.cur.execute(q_valid, [d["geom"], EPSG_CODE])
            valid_result = self.cur.fetchall()

            if not valid_result or valid_result[0][0] is not True:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "Geometría inválida",
                    "data": None
                }

            q_within = """
            SELECT id
            FROM d.barrios
            WHERE ST_Within(
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                ),
                geom
            )
            """
            self.cur.execute(q_within, [d["geom"], EPSG_CODE])
            within_result = self.cur.fetchall()

            if len(within_result) == 0:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "El punto está fuera de cualquier barrio",
                    "data": None
                }

            cons = """
            UPDATE d.clientes
            SET
                nombre = %s,
                direccion = %s,
                telefono = %s,
                tipo_cliente = %s,
                barrio = %s,
                geom = ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                )
            WHERE id = %s
            """

            self.cur.execute(cons, [
                d["nombre"],
                d["direccion"],
                d["telefono"],
                d["tipo_cliente"],
                d["barrio"],
                d["geom"],
                EPSG_CODE,
                d["id"]
            ])

            rows_updated = self.cur.rowcount
            self.conn.commit()

            self.disconnect()

            return {
                "ok": True,
                "message": "Datos actualizados correctamente",
                "data": [{"rows_updated": rows_updated}]
            }

        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def delete(self, d):
        try:
            cons = """
            DELETE FROM d.clientes
            WHERE id = %s
            """

            self.cur.execute(cons, [d["id"]])

            rows_deleted = self.cur.rowcount
            self.conn.commit()

            self.disconnect()

            return {
                "ok": True,
                "message": "Datos eliminados correctamente",
                "data": [{"rows_deleted": rows_deleted}]
            }

        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }
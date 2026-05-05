from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class RutasOOP():

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

            q_intersection = """
            SELECT id
            FROM d.rutas
            WHERE ST_Intersects(
                geom,
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                )
            )
            """
            self.cur.execute(q_intersection, [d["geom"], EPSG_CODE])
            inter_result = self.cur.fetchall()

            if len(inter_result) > 0:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "La línea intersecta con otras rutas",
                    "data": None
                }

            cons = """
            INSERT INTO d.rutas
                (geom, distancia, tiempo, estado, barrio_destino, numero_paradas)
            VALUES
                (
                 ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                 ),
                 %s, %s, %s, %s, %s
                )
            RETURNING id
            """

            self.cur.execute(cons, [
                d["geom"],
                EPSG_CODE,
                d["distancia"],
                d["tiempo"],
                d["estado"],
                d["barrio_destino"],
                d["numero_paradas"]
            ])

            self.conn.commit()
            l = self.cur.fetchall()

            self.disconnect()

            return {
                "ok": True,
                "message": "Ruta insertada correctamente",
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
            SELECT id, ST_AsText(geom), distancia, tiempo, estado, barrio_destino, numero_paradas
            FROM d.rutas
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
            SELECT id, ST_AsText(geom) AS geom, distancia, tiempo, estado, barrio_destino, numero_paradas
            FROM d.rutas
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

            q_intersection = """
            SELECT id
            FROM d.rutas
            WHERE ST_Intersects(
                geom,
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                )
            )
            AND id != %s
            """
            self.cur.execute(q_intersection, [d["geom"], EPSG_CODE, d["id"]])
            inter_result = self.cur.fetchall()

            if len(inter_result) > 0:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "La línea intersecta con otras rutas",
                    "data": None
                }

            cons = """
            UPDATE d.rutas
            SET
                geom = ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                ),
                distancia = %s,
                tiempo = %s,
                estado = %s,
                barrio_destino = %s,
                numero_paradas = %s
            WHERE id = %s
            """

            self.cur.execute(cons, [
                d["geom"],
                EPSG_CODE,
                d["distancia"],
                d["tiempo"],
                d["estado"],
                d["barrio_destino"],
                d["numero_paradas"],
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
            DELETE FROM d.rutas
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
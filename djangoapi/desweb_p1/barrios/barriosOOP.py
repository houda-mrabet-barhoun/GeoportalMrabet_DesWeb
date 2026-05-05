from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class BarriosOOP():

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
            FROM d.barrios
            WHERE ST_Relate(
                geom,
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                ),
                'T********'
            )
            """
            self.cur.execute(q_intersection, [d["geom"], EPSG_CODE])
            inter_result = self.cur.fetchall()

            if len(inter_result) > 0:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "El polígono intersecta con otros barrios",
                    "data": None
                }

            cons = """
            INSERT INTO d.barrios
                (nombre, codigo, distrito, geom, area, numero_clientes)
            VALUES
                (%s, %s, %s,
                 ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                 ),
                 %s, %s
                )
            RETURNING id
            """

            self.cur.execute(cons, [
                d["nombre"],
                d["codigo"],
                d["distrito"],
                d["geom"],
                EPSG_CODE,
                d["area"],
                d["numero_clientes"]
            ])

            self.conn.commit()
            l = self.cur.fetchall()

            self.disconnect()

            return {
                "ok": True,
                "message": "Barrio insertado correctamente",
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
            SELECT id, nombre, codigo, distrito, ST_AsText(geom), area, numero_clientes
            FROM d.barrios
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
            SELECT id, nombre, codigo, distrito, ST_AsText(geom) AS geom, area, numero_clientes
            FROM d.barrios
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
            FROM d.barrios
            WHERE ST_Relate(
                geom,
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                ),
                'T********'
            )
            AND id != %s
            """
            self.cur.execute(q_intersection, [d["geom"], EPSG_CODE, d["id"]])
            inter_result = self.cur.fetchall()

            if len(inter_result) > 0:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "El polígono intersecta con otros barrios",
                    "data": None
                }

            cons = """
            UPDATE d.barrios
            SET
                nombre = %s,
                codigo = %s,
                distrito = %s,
                geom = ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    0.0001
                ),
                area = %s,
                numero_clientes = %s
            WHERE id = %s
            """

            self.cur.execute(cons, [
                d["nombre"],
                d["codigo"],
                d["distrito"],
                d["geom"],
                EPSG_CODE,
                d["area"],
                d["numero_clientes"],
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
            DELETE FROM d.barrios
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
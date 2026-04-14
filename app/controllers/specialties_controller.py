import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.specialties_model import Specialties
from fastapi.encoders import jsonable_encoder

class SpecialtiesController:

    def create_specialty(self, specialty: Specialties):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO specialties (name)
                VALUES (%s)
            """, (specialty.name,))
            conn.commit()
            return {"resultado": "Specialty created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_specialty(self, specialty_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM specialties WHERE id = %s", (specialty_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'specialty_id': int(result[0]),
                    'name': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Specialty not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_specialties(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM specialties")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'specialty_id': data[0],
                    'name': data[1]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No specialties found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_specialty(self, specialty_id: int, specialty: Specialties):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE specialties
                SET name = %s
                WHERE id = %s
                RETURNING id, name;
            """, (specialty.name, specialty_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'specialty_id': int(result[0]),
                    'name': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Specialty not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_specialty(self, specialty_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM specialties
                WHERE id = %s
                RETURNING id, name;
            """, (specialty_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'specialty_id': int(result[0]),
                    'name': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Specialty not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
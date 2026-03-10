import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.groups_model import Groups
from fastapi.encoders import jsonable_encoder

class GroupsController:

    def create_group(self, group: Groups):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO groups (section, shift, num_students, subject_id)
                VALUES (%s, %s, %s, %s)
            """, (group.section, group.shift, group.num_students, group.subject_id))
            conn.commit()
            return {"resultado": "Group created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_group(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM groups WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': int(result[0]),
                    'section': result[1],
                    'shift': result[2],
                    'num_students': int(result[3]),
                    'subject_id': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Group not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_groups(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM groups")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'section': data[1],
                    'shift': data[2],
                    'num_students': data[3],
                    'subject_id': data[4]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No groups found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_group(self, id: int, group: Groups):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE groups
                SET section = %s,
                    shift = %s,
                    num_students = %s,
                    subject_id = %s
                WHERE id = %s
                RETURNING id, section, shift, num_students, subject_id;
            """, (group.section, group.shift, group.num_students, group.subject_id, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'section': result[1],
                    'shift': result[2],
                    'num_students': int(result[3]),
                    'subject_id': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Group not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_group(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM groups
                WHERE id = %s
                RETURNING id, section, shift, num_students, subject_id;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'section': result[1],
                    'shift': result[2],
                    'num_students': int(result[3]),
                    'subject_id': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Group not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
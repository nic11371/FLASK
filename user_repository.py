from psycopg2.extras import RealDictCursor
import psycopg2
# dbname='nikolay', user='nikolay', password='12345', host='localhost'


class UserRepository():
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM users")
                return c.fetchall()

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM users WHERE id = %s", (id,))
                return c.fetchone()

    def destroy(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("DELETE FROM users WHERE id = %s", (id,))
            conn.commit()

    def save(self, user):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                if 'id' not in user:
                    c.execute(
                        """INSERT INTO users (name, email) VALUES (%s, %s)
                        RETURNING id""",
                        (user['name'], user['email'])
                    )
                    user['id'] = c.fetchone()[0]
                else:
                    c.execute(
                        "UPDATE users SET name = %s, email = %s WHERE id = %s",
                        (user['name'], user['email'], user['id'])
                    )
            conn.commit()
        return user['id']

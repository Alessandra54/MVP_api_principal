import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receitas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    ingredientes TEXT NOT NULL
                )
            ''')
            conn.commit()

    def get_receitas(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM receitas")
            receitas = cursor.fetchall()
        return [{"id": r[0], "nome": r[1], "ingredientes": r[2]} for r in receitas]

    def add_receita(self, nome, ingredientes):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO receitas (nome, ingredientes) VALUES (?, ?)", (nome, ingredientes))
            conn.commit()

    def update_receita(self, id, nome, ingredientes):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE receitas SET nome = ?, ingredientes = ? WHERE id = ?", (nome, ingredientes, id))
            conn.commit()

    def delete_receita(self, id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM receitas WHERE id = ?", (id,))
            conn.commit()

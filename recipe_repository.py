import sqlite3
import queue


class RecipeRepository:

    def __init__(self):
        self.db_path = "recipes.db"
        self.setup_db()

    def setup_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe TEXT,
                    retries INTEGER DEFAULT 0,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_attempt TIMESTAMP
                )
            """
            )
            conn.commit()

    def load_queue(self):
        q = queue.Queue()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, recipe, retries FROM recipes WHERE processed = FALSE AND retries < 3"
            )
            recipes = cursor.fetchall()
            for recipe_id, recipe, retries in recipes:
                q.put((recipe_id, recipe, retries))
        return q

    def mark_as_processed(self, recipe_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE recipes 
                SET processed = TRUE, last_attempt = CURRENT_TIMESTAMP 
                WHERE id = ?
                """,
                (recipe_id,),
            )
            conn.commit()

    def increment_retries(self, recipe_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE recipes 
                SET retries = retries + 1, last_attempt = CURRENT_TIMESTAMP 
                WHERE id = ?
                """,
                (recipe_id,),
            )
            conn.commit()

    def remove_processed_items(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipes WHERE processed = TRUE")
            conn.commit()

    def add_new_items(self, items):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO recipes (recipe, retries, processed, created_at) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """,
                [(item, 0, False) for item in items],
            )
            conn.commit()

    def get_retries(self, recipe_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT retries FROM recipes WHERE id = ?", (recipe_id,))
            retries = cursor.fetchone()
            return retries[0] if retries else 0

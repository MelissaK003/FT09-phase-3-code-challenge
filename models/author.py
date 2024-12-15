from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    all = {}

    def __init__(self, id, name):
        from models.article import Article
        # Validate name input
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must be longer than 0 characters")

        # Initialize attributes
        self._id = id
        self._name = name

        # Save to the database if id is None
        if self._id is None:
            self.save()

        # Save instance to the class dictionary
        type(self).all[self.id] = self

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save(self):
        """Save the author to the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """
        cursor.execute(sql, (self.name,))
        conn.commit()
        self._id = cursor.lastrowid
        cursor.close()
        conn.close()
        type(self).all[self.id] = self

    @classmethod
    def find_by_id(cls, author_id):
        """Find an author by their ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT id, name
            FROM authors
            WHERE id = ?
        """
        cursor.execute(sql, (author_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return cls(*row)
        return None

    def articles(self):
        """Return all articles associated with the author using SQL JOIN."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Article(*row) for row in rows]

    def magazines(self):
        """Return all magazines associated with the author using SQL JOIN."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Magazine(*row) for row in rows]

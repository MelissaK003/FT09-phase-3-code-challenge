from models.article import Article
from models.author import Author
from database.connection import get_db_connection

class Magazine:
    all = {}

    def __init__(self, id, name, category):
        # Validate name
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")

        # Validate category
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")

        self._id = id
        self._name = name
        self._category = category

        # Save to database if id is None
        if self._id is None:
            self.save()

        # Add instance to class dictionary
        type(self).all[self.id] = self

    def save(self):
        """Save the magazine to the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        cursor.close()
        conn.close()
        type(self).all[self.id] = self

    def __repr__(self):
        return f"<Magazine {self.name}>"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        """Return all articles associated with this magazine using SQL JOIN."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT id, title, content, author_id, magazine_id
            FROM articles
            WHERE magazine_id = ?
        """
        cursor.execute(sql, (self.id,))
        articles = [Article(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return articles

    def contributors(self):
        """Return all distinct authors who have articles in this magazine using SQL JOIN."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """
        cursor.execute(sql, (self.id,))
        contributors = [Author(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return contributors

    def article_titles(self):
        """Return a list of article titles for this magazine, or None if no articles exist."""
        articles = self.articles()
        if articles:
            return [article.title for article in articles]
        return None

    def contributing_authors(self):
        """Return authors who have written more than 2 articles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id, a.name
            HAVING COUNT(ar.id) > 2
        """
        cursor.execute(sql, (self.id,))
        authors = [Author(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return authors if authors else None

from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    all = {}

    def __init__(self, id, title, content, author, magazine):
        from models.author import Author
        # Ensures the title is a string
        if not isinstance(title, str):
            raise TypeError("Invalid Title input")
        # Ensures the length of the title is between 5 and 50 characters
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        # Validate content
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Content must be a non-empty string")
        # Validate that both the author and magazine have a name attribute
        if not hasattr(author, 'name'):
            raise TypeError("Invalid Author")
        if not hasattr(magazine, 'name'):
            raise TypeError("Invalid Magazine")

        # Initialize attributes
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author.id
        self._magazine_id = magazine.id

        # Save to the database if id is None
        if self._id is None:
            self.save()

        # Save instance to the class dictionary
        type(self).all[self.id] = self

    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    @property
    def author(self):
        """Retrieve the author associated with this article using a SQL JOIN."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        """
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Author(row[0], row[1])
        return None

    @property
    def magazine(self):
        """Retrieve the magazine associated with this article using a SQL JOIN."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        """
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Magazine(row[0], row[1], row[2])
        return None

    def save(self):
        """Save the article to the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        conn.commit()
        self._id = cursor.lastrowid
        cursor.close()
        conn.close()
        type(self).all[self.id] = self

    @classmethod
    def create(cls, title, content, author, magazine):
        """Create and save a new article."""
        article = cls(None, title, content, author, magazine)
        return article

    def update(self, new_content):
        """Update the article's content."""
        if not isinstance(new_content, str) or len(new_content) == 0:
            raise ValueError("Content must be a non-empty string")

        self._content = new_content
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE articles
            SET content = ?
            WHERE id = ?
        """
        cursor.execute(sql, (self.content, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """Delete the article from the database and the class dictionary."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            DELETE FROM articles
            WHERE id = ?
        """
        cursor.execute(sql, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()
        del type(self).all[self.id]

    @classmethod
    def find_by_id(cls, article_id):
        """Find an article by its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT id, title, content, author_id, magazine_id
            FROM articles
            WHERE id = ?
        """
        cursor.execute(sql, (article_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return cls(*row)
        return None

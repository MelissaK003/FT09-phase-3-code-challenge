from database.connection import get_db_connection
from models.article import Article  

class Magazine:
    def __init__(self, id, name, category):
        # Ensure the name is a string between 2 and 16 characters
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be between 2 and 16 characters")
        #Ensure Id is an integer
        if not isinstance(id, int):
            raise TypeError("ID must be an integer")
        # Ensure the category is a non-empty string
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must not be empty ")

        # Initialize attributes
        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category
    
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT article.id, article.title, article.author_id, article.magazine_id
            FROM articles article
            JOIN magazines magazine ON article.magazine_id = magazine.id
            WHERE magazine.id = ?
        """
        cursor.execute(sql, (self.id,))
        articles = [Article(*row) for row in cursor.fetchall()]  
        cursor.close()
        conn.close()
        return articles
    
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT article.title
            FROM articles article
            JOIN magazines magazine ON a.magazine_id = magazine.id
            WHERE magazine.id = ?
        """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        if not rows:
            return None
        
    def __repr__(self):
        return f'<Magazine {self.name}>'

from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, id, name):
        # Ensures the name is a string
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        # Ensures the length of the name is > 0
        if len(name) == 0:
            raise ValueError("Name must not be empty")
        if not isinstance(id, int):
            raise TypeError("ID must be an integer")
        
        self._id = id
        self._name = name

    #Gets the Author id and name
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    #Prevent the name from being changed after instantiation.
    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed ")

    #Return all articles associated with this author. 
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT article.id, article.title, article.author_id, article.magazine_id
            FROM articles article
            JOIN authors au ON article.author_id = author.id
            WHERE author.id = ?
        """
        cursor.execute(sql, (self.id,))
        articles = [Article(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return articles

    #Return the magazine associated with this article. 
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT magazine.id, magazine.name, magazine.category
            FROM magazines magazine
            JOIN articles article ON article.magazine_id = magazine.id
            WHERE article.id = ?
        """
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Magazine(*row)  
        return None

    def __repr__(self):
        return f'<Author {self.name}>'

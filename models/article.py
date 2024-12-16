
class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        # Ensure the title is a string
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        # Ensure the title is between 5 and 50 characters
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        
        # Initialize attributes
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self):
        if hasattr(self, '_title'):
            raise AttributeError("Title cannot be changed after instantiation")
    
                        
    def __repr__(self):
        return f'<Article {self.title}>'
    
    
    
   
from app.storage.category_storage import CategoryStorage

class CategoryService:
    def __init__(self):
        self.storage = CategoryStorage()

    def get_categories(self):
        return self.storage.get_categories()
    
    def add_category(self, data):
        category = data.get('category', '').strip()

        if not category:
            return {"error": "Invalid category"}, 400
        
        if category in self.storage._CATEGORIES_CACHE:
            return {"error": "Category already exists"}, 400
        
        self.storage.add_category(category)
        return {"message": "Category added successfully"}, 201
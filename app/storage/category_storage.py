

class CategoryStorage:

    CATEGORIES = []

    def __init__(self):
        self.load_categories_from_txt()

    def load_categories_from_csv(self, category):
        category = category.strip()
        if category and category not in self.CATEGORIES:
            self.CATEGORIES.append(category)
        return self.CATEGORIES
    
    def load_categories_from_txt(self):
        try:
            with open('categories.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and line not in self.CATEGORIES:
                        self.CATEGORIES.append(line)
        except FileNotFoundError:
            pass
    
    def get_categories(self):
        if not self.CATEGORIES:
            try:
                with open('categories.txt', 'r') as f:
                    self.CATEGORIES = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                pass
        return self.CATEGORIES

    def add_category(self, category):
        if category and category not in self.CATEGORIES:
            self.CATEGORIES.append(category)
            self.update_categories_file()


    def update_categories_file(self):
        with open('categories.txt', 'w') as f:
            for category in self.CATEGORIES:
                f.write(category + '\n')
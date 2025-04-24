import os
import threading
from flask import current_app

class CategoryStorage:

    _CATEGORIES_CACHE = None
    _cache_lock = threading.Lock()

    def __init__(self):
        #self.load_categories_from_txt()
        print("DEBUG: CategoryStorage instance created (cache not loaded yet)")
        pass

    def _load_categories_if_needed(self):
        with CategoryStorage._cache_lock:
            if CategoryStorage._CATEGORIES_CACHE is None:
                print("DEBUG: Cache is None, attempting to load categories...")
                self.load_categories_from_txt()

    def load_categories_from_txt(self):
        file_path = self._get_category_file_path()

        if file_path is None:
            print("ERROR: Skipping category loading because file path could not be determined.")
            type(self)._CATEGORIES_CACHE = []
            return
        
        print(f"Attempting to load categories from: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_categories = [line.strip() for line in f if line.strip()]
                type(self)._CATEGORIES_CACHE = loaded_categories
                print(f"Loaded categories: {type(self)._CATEGORIES_CACHE}")

        except FileNotFoundError:
            print(f"Category file not found at {file_path}. Starting with empty list.")
            type(self)._CATEGORIES_CACHE = [] 
        
        except Exception as e:
            #Catch other potential file reading errors
            print(f"An error occurred reading {file_path}: {e}")
            type(self)._CATEGORIES_CACHE = [] # Reset cache on error


    def _get_instance_path(self):
        # Gets the absolute path to the Flask instance folder
        try:
            instance_path = current_app.instance_path
            print(f"DEBUG: Found instance path: {instance_path}")
            return instance_path
        except RuntimeError as e:
            print(f"ERROR: Coult not get instance path. Is Flask app context active? {e}")
            return None
        
    def _get_category_file_path(self):
        #Builds the full absolute path to categories.txt in the instance folder
        instance_folder_path = self._get_instance_path()

        if instance_folder_path is None:
            print("Error: Cannot build category file path because instance path is unknown.")
            return None
        
        full_path = os.path.join(instance_folder_path, 'categories.txt')
        print(f"DEBUG: Calculated category file path: {full_path}") # Debug log
        return full_path

    def load_categories_from_csv(self, category):
        category = category.strip()
        if category and category not in self._CATEGORIES_CACHE:
            self._CATEGORIES_CACHE.append(category)
        return self._CATEGORIES_CACHE
    
    def load_categories_from_txt(self):
        file_path = self._get_category_file_path()

        if file_path is None:
            print("ERROR: Skipping category loading because file path could not be determined.")
            type(self)._CATEGORIES_CACHE = []
            return
        
        if not type(self)._CATEGORIES_CACHE:
            print(f"Attempting to load categories from: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_categories = [line.strip() for line in f if line.strip()]
                    type(self)._CATEGORIES_CACHE = loaded_categories
                    print(f"Loaded categories: {type(self)._CATEGORIES_CACHE}")

            except FileNotFoundError:
                print(f"Category file not found at {file_path}. Starting with empty list.")
                type(self)._CATEGORIES_CACHE = [] 
            
            except Exception as e:
                #Catch other potential file reading errors
                print(f"An error occurred reading {file_path}: {e}")
                type(self)._CATEGORIES_CACHE = [] # Reset cache on error
    
    def get_categories(self):
        self._load_categories_if_needed()
        return self._CATEGORIES_CACHE

    def add_category(self, category):
        # Ensure cache is loaded before checking/modifying
        self._load_categories_if_needed()

        with CategoryStorage._cache_lock:
            if category not in CategoryStorage._CATEGORIES_CACHE:
                CategoryStorage._CATEGORIES_CACHE.append(category)
                print(f"DEBUG: Category '{category}' added to cache.")
                self.update_categories_file()
            else:
                print(f"DEBUG: Category '{category}' already exists in cache, not adding.")


    def update_categories_file(self):
        if CategoryStorage._CATEGORIES_CACHE is None:
            print("ERROR: Cannot save categories, cache was never initialized.")
            return
        
        file_path = self._get_category_file_path()

        if file_path is None:
            print("ERROR: Cannot save categories because file path could not be determined.")
            return
        
        print(f"Attempting to save categories to: {file_path}")
        try:
            #check that instance folder exists
            instance_folder = os.path.dirname(file_path)
            os.makedirs(instance_folder, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                for category in type(self)._CATEGORIES_CACHE:
                    f.write(category + '\n')
            print("Categories saved successfully.")

        except Exception as e:
            print(f"ERROR saving categories to {file_path}: {e}")


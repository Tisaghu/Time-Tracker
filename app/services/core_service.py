from flask import render_template

class CoreService:
    def get_index(self):
        return render_template('index.html')

    def get_test_message(self):
        return "The core blueprint is working!"

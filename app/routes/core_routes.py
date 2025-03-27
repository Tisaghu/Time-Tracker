from flask import Blueprint, render_template
from app.services.core_service import CoreService

core_bp = Blueprint('core', __name__)
core_service = CoreService()

@core_bp.route('/')
def index():
    return core_service.get_index()

@core_bp.route('/test')
def test():
    return core_service.get_test_message()

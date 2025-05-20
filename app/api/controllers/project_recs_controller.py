from flask import request, Blueprint, jsonify
from services.projectRecs_service import project_recs

project_recs_bp = Blueprint('project_recs_bp', __name__)

@project_recs_bp.route('/recommend', methods=['POST'])
def recommend():
    employee_info = request.json.get("employeeInfo")
    available_projects = request.json.get("availableProjects")
    return project_recs(employee_info, available_projects)
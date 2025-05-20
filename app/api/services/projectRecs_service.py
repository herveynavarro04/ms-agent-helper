import os
import json
import requests
from flask import request, jsonify

def project_recs(employee_info, available_projects):
    api_key = os.getenv("API_KEY")
    url = os.getenv("URL", "https://api.openai.com/v1/chat/completions")

    if not employee_info or not available_projects:
        return jsonify({"error": "'employee_info' and 'availableProjects' are required"}), 400

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
        "content": (
            "You are a recommendation engine that selects the 5 most relevant projects for an employee. "
            "You will receive the employee's profile, including their skills, interests, and past project descriptions, "
            "as well as a list of available projects (each with an ID and description). "
            "Evaluate all three factors — skills, interests, and past projects — when selecting projects. "
            "Assign the highest weight to interests, followed by past projects, and then skills. "
            "All selections must be coherent and relevant to the employee's profile. "
            "Inject light randomness so that results may differ across requests, but only among suitable matches. "
            "Return ONLY a JSON object with the format: {\"projects\": [\"id1\", \"id2\", \"id3\", \"id4\", \"id5\"]}. "
            "Do not include any explanation or additional text — only the JSON object."
        )
            },
            {
                "role": "user",
                "content": json.dumps({
                    "employee_info": employee_info,
                    "available_projects": available_projects
                })
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "projects" in parsed and isinstance(parsed["projects"], list):
                return jsonify(parsed)
            else:
                return jsonify({"error": "Invalid format returned by model"}), 500

        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

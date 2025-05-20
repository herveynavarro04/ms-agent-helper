from flask import Flask
from dotenv import load_dotenv

load_dotenv()  

from controllers.project_recs_controller import project_recs_bp  

app = Flask(__name__)
app.register_blueprint(project_recs_bp, url_prefix='/api/agent')  

if __name__ == '__main__':
    app.run(debug=True)
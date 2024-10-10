from flask import jsonify
from vanna.flask import VannaFlaskApp
from flask_cors import CORS


from src.model import vanna

app = VannaFlaskApp(
    vanna,
    allow_llm_to_see_data=True,
    title="NQL",
    subtitle="SQL queries con lenguaje natural",
)
CORS(app.flask_app)

run_app = app.flask_app
# app.run(host='0.0.0.0')

@run_app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify(status="healthy"), 200

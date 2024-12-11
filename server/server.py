from flask import Flask, request, jsonify
from gen_ai_hub.proxy.langchain import init_llm
from langchain_core.language_models import BaseLanguageModel

from DB.db_types import DBType
from DB.settings import VectorDBSettings
from DB.utils import add_github_repo_to_db
from DB.vector_db import VectorDB
from scanners.github.github_scanner import GitHubScanner
from scanners.github.github_settings import GitHubSettings

app = Flask(__name__)


# API endpoint 1: Query endpoint
@app.route('/query', methods=['GET'])
def query():
    query_param = request.args.get('query')
    if not query_param:
        return jsonify({"error": "Missing required query parameter 'query'."}), 400
    return jsonify({"message": f"You searched for: {query_param}"})


# API endpoint 2: GitHub info endpoint
@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    required_keys = ['github_url', 'github_repo_name', 'user_name', 'github_token']

    if not data or not all(key in data for key in required_keys):
        return jsonify({
                           "error": "Invalid input. Please provide 'github_url', 'github_repo_name', 'user_name', and 'github_token'."}), 400

    github_url = data['github_url']
    github_repo_name = data['github_repo_name']
    user_name = data['user_name']
    github_token = data['github_token']

    github_settings = GitHubSettings(user_name, github_token, github_repo_name, github_url)
    github_scanner = GitHubScanner(github_settings)

    # init VectorDB
    db_api_key = "p6ErOJYvqi-daabdLArES-QeBxAxfGYzE46i40ML1hx-5unp7DUFUA"
    db_url = "https://bac12217-a8c1-42c2-96a2-d60825ac7f4d.us-west-2-0.aws.cloud.qdrant.io:6333"
    settings = VectorDBSettings(db_type=DBType.QDRANT, url=db_url, api_key=db_api_key)
    vector_db = VectorDB(settings)

    # init LLM
    llm: BaseLanguageModel = init_llm('gpt-4o')

    # add github repo to vectorDB
    add_github_repo_to_db(github_scanner=github_scanner, vector_db=vector_db, llm=llm)

    # Placeholder logic to process the GitHub information
    return jsonify({
        "message": "GitHub information received successfully."
    })


if __name__ == '__main__':
    app.run(debug=True)

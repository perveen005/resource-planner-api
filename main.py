import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv  


load_dotenv()

app = Flask(__name__)


azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")


openai.api_key = azure_openai_key
openai.api_base = azure_openai_endpoint
openai.api_type = 'azure'
openai.api_version = '2023-05-15'
deployment_name = 'davinci-trial'


app = Flask(__name__)

def calculate_match_percentage(job_description, candidate_profile):
    prompt = f"Job Description: {job_description}\n\nCandidate skills: {candidate_profile}\n\nCompute the match percentage between the job description and candidate skills. More number of candidate skills present in the job description, the higher the match score should be."

    response = openai.Completion.create(
        engine=deployment_name,
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )

    generated_text = response.choices[0].text.strip()
    match_percentage = str(generated_text.split(":")[-1].strip().replace("%", ""))
    return match_percentage

@app.route('/calculate_match', methods=['POST'])
def api_calculate_match_percentage():
    data = request.get_json()
    job_description = data.get('job_description')
    candidate_profile = data.get('candidate_profile')
    if job_description and candidate_profile:
        match_percentage = calculate_match_percentage(job_description, candidate_profile)
        return jsonify({"match_percentage": match_percentage})
    else:
        return jsonify({"error": "Missing job_description or candidate_profile in the request"}), 400

if __name__ == "__main__":
    app.run(debug=True)

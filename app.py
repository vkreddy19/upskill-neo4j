from flask import Flask, render_template, jsonify, make_response
from flask import request
from pyresparser import ResumeParser
from werkzeug.utils import secure_filename
from py2neo import Graph

app = Flask("Upskill")
g = Graph("bolt://localhost:11003", password="vamshi19")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/autocomplete', methods=['GET', 'POST', 'PUT'])
def search():
    search= request.form.get('search', "")
    if search:
        res = g.run('match (n:Job)-[rel]->(:Skill) where n.normalized_job_title contains "%s" return n.normalized_job_title as result,  count(rel) as rels  order by rels DESC limit 10;'%search)
        return jsonify([x[0] for x in res])
    else:
        return jsonify([])


def _get_skills_from_resume(file="uploads/latest_uploaded_resume.docx"):
    data = ResumeParser(file).get_extracted_data()
    return [x.lower() for x in data.get('skills', [])]


@app.route('/analyze', methods=['GET', 'POST', 'PUT'])
def analyze():
    role = request.form.get('role', "").lower()
    print(role)
    resume_skills = _get_skills_from_resume()
    res = get_related_jobs(role)
    print(res)
    result = []
    for role in res:
        required_skills = role[1]
        missing_skills = [x for x in required_skills if x not in resume_skills]
        matching_skills = [x for x in required_skills if x in resume_skills]
        if not matching_skills or not required_skills:
            continue
        per_match = (len(matching_skills)/len(required_skills))*100
        result.append({'missing_skills': missing_skills,
                       'matching_skills': matching_skills,
                       'percentage_match': per_match,
                       'role': role[0]})

    return jsonify(result)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('uploads/latest_uploaded_resume')
    return "True"

def get_related_jobs(job_title):
    query = 'match (:Job {normalized_job_title: "%s"})-[:related]-(n:Job)-[r:need]-(d:Skill) where toFloat(d.importance)>2 with n, collect(d.skill_name) as s, collect(d.importance) as imp return  n,s, imp  limit 5;'%job_title
    res = g.run(query)
    return res

app.run(port=8082, debug=True)

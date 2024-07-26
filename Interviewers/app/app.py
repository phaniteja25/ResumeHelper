from flask import Flask,render_template, request
import os
import helper_func as helper_func 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads/"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

@app.route("/")
def matchResume():
    return render_template("simlarity_checker.html")


@app.route("/matcher",methods=["GET","POST"])
def matcher():

    if request.method == 'POST':
        
        job_desc = request.form.get("job_description")

        top_n_resume = int(request.form.get("top_n_resume"))

        resumes_list = request.files.getlist("resumes")
    
        resumes = []

        for resume in resumes_list:
            filename = os.path.join(app.config["UPLOAD_FOLDER"],resume.filename)
            print(filename)
            resume.save(filename)
            resumes.append(helper_func.extract_text(filename))
        
        
        #Vectorizing Job Description and resumes
        vectorizer = TfidfVectorizer().fit_transform([job_desc] + resumes)
        vectors = vectorizer.toarray()

        

        #calculate cosine similarities

        job_vector = vectors[0]
        resume_vector = vectors[1:]
        
        similarities = cosine_similarity([job_vector],resume_vector)[0]

        similarities = np.array(similarities)
        #extracting the indices of three resumes 
        top_indices = similarities.argsort()[-top_n_resume:][::-1]

        top_resumes = [resumes_list[i].filename for i in top_indices]   

        similarity_scores = [round(similarities[i],2) for i in top_indices]   

    return render_template('simlarity_checker.html', message="Here is the result:", top_resumes=top_resumes, similarity_scores=similarity_scores)
  


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        file = request.files.get("pdf_file")

        if file and file.filename:
            file.save(f"./uploads/{file.filename}")
            
            return render_template("index.html", message="File uploaded successfully!")
        
        return render_template("index.html", message="Please, select a PDF file first.")

    return render_template("index.html")
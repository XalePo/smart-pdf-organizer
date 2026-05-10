from flask import Flask, render_template, request
from pypdf import PdfReader


def main():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def welcome():
        if request.method == "POST":
            file = request.files.get("pdf_file")

            if file and file.filename:
                file_name = file.filename
                file_path = save_uploaded_file(file)
                pdf_info = extract_pdf_info(file_path)
                
                # TO DO
                keywords = extract_keywords(file_name, pdf_info)


                return render_template("index.html", message="File uploaded and analyzed successfully.")
            
            

        return render_template("index.html")


    def save_uploaded_file(file):
        path = f"./uploads/{file.filename}"
        file.save(path)
        
        return path
        
    
    def extract_pdf_info(saved_path):
        reader = PdfReader(saved_path)
        page = reader.pages[0]
        text = page.extract_text()
        return text

    
    def extract_keywords(file_name, pdf_info):
        ...

    
    app.run(debug=True)
if __name__ == "__main__":
    main()

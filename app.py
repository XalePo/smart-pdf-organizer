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
                
                keywords = extract_keywords(file_name, pdf_info)


                return render_template("index.html", message="File uploaded and analyzed successfully.")
            
            

        return render_template("index.html")


    def save_uploaded_file(file) -> str:
        path = f"./uploads/{file.filename}"
        file.save(path)
        
        return path
        
    
    def extract_pdf_info(saved_path) -> str:
        reader = PdfReader(saved_path)
        page = reader.pages[0]
        text = page.extract_text()
        print(text)
        return text

    
    def extract_keywords(file_name, pdf_info):
        subject_keywords = {
            "calculus" : {"mathematics", "derivative", "mac", "function"},
            "composition" : {"essay", "enc", "citation", "paragraph"},
            "physics" : {"force", "velocity", "phy", "acceleration", "energy"},
            "programming" : {"python", "cop", "flask", "function", "class"},
        }
        
        combined_text = f"{file_name} {pdf_info or  ' '}".lower()
        scores = {}

        for subject, keywords in subject_keywords.items():
            for keyword in keywords:
                if keyword in combined_text:
                    scores[subject] = scores.get(subject, 0) + 1

        if not scores:
            return "unknown"
        
        return max(scores, key=scores.get)
            

    app.run(debug=True)
if __name__ == "__main__":
    main()

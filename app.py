from flask import Flask, render_template, request
from pypdf import PdfReader
from pathlib import Path
import shutil


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
                subject = extract_keywords(file_name, pdf_info)

                suggested_path = display_folder(subject)

                return render_template(
                    "index.html", 
                    message="File uploaded and analyzed successfully.", 
                    subject=subject, 
                    suggested_path=suggested_path,
                    file_path=file_path,
                )

            return render_template(
                "index.html",
                message="Please, select a PDF first."
            )
            
        return render_template("index.html")


    @app.route("/move", methods=["POST"])
    def move_file():
        file_path = request.form.get("file_path")
        suggested_path = request.form.get("suggested_path")
        subject = request.form.get("subject")

        if not file_path or not suggested_path:
            return render_template(
                "index.html",
                message="Missing file path or destination path. Please upload the PDF again."
            )

        current_path = Path(file_path)
        destination_path = Path(suggested_path)

        if not current_path.exists():
            return render_template(
                "index.html",
                message="This file was already moved or no longer exists. Please upload it again."
            )

        destination_path.mkdir(parents=True, exist_ok=True)
        final_path = destination_path / current_path.name

        shutil.move(current_path, final_path)

        return render_template(
            "index.html",
            message="File moved successfully.",
            subject=subject,
            final_path=final_path
        )


    def save_uploaded_file(file) -> str:
        path = f"./uploads/{file.filename}"
        file.save(path)
        
        return path
        
    
    def extract_pdf_info(saved_path) -> str:
        reader = PdfReader(saved_path)
        page = reader.pages[0]
        text = page.extract_text()
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
            

    def display_folder(subject):
        folder_paths = {
            "calculus": "/Users/alejandromorales/College/MDC/Courses/Calculus I",
            "composition": "/Users/alejandromorales/College/MDC/Courses/Composition I",
            "physics": "/Users/alejandromorales/College/MDC/Courses/Physics I",
            "programming": "/Users/alejandromorales/Programming", 
            "unknown": "/Users/alejandromorales/Downloads"
        }

        return folder_paths.get(subject, folder_paths["unknown"])


    app.run(debug=True)
if __name__ == "__main__":
    main()

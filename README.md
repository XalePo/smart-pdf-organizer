# Smart PDF Organizer

Smart PDF Organizer is a simple Flask web app that lets users upload a PDF, read the first page, suggest a category based on basic keywords, and move the file to a matching folder.

It is a beginner project built to practice Flask routes, HTML forms, file uploads, PDF reading, and basic file organization.

## Features

- Upload a PDF file
- Read text from the first page using `pypdf`
- Analyze the file name and PDF text using simple keyword matching
- Suggest a category such as:
  - Calculus
  - Composition
  - Physics
  - Programming
  - Unknown
- Show the suggested destination folder
- Move the PDF after confirmation
- Display the final file location

## Tech Used

- Python
- Flask
- pypdf
- HTML
- CSS

## Project Structure

```text
smart-pdf-organizer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   └── styles.css
│
└── uploads/
```

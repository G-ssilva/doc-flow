from flask import Flask, render_template, request, send_file
from main import gerar_documento
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "saida"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    download_links = []

    if request.method == "POST":
        pdf_files = request.files.getlist("pdfs")

        for pdf_file in pdf_files:
            caminho_pdf = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(caminho_pdf)

            saida_docx = gerar_documento(caminho_pdf, output_dir=OUTPUT_FOLDER)
            download_links.append(os.path.basename(saida_docx))

    return render_template("index.html", download_links=download_links)


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

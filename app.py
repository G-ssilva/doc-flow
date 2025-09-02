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
    if request.method == "POST":
        pdf_file = request.files["pdf"]
        caminho_pdf = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(caminho_pdf)

        saida_docx = gerar_documento(caminho_pdf, output_dir=OUTPUT_FOLDER)
        return send_file(saida_docx, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

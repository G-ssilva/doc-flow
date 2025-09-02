import re
import pytesseract
from pdf2image import convert_from_path
from docxtpl import DocxTemplate
from datetime import datetime
import locale
import os

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def extrair_campo(pattern, text, group=1):
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return match.group(group).strip() if match else ""

def gerar_documento(pdf_path, modelo_docx="modelo.docx", output_dir="saida"):
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)
    texto = pytesseract.image_to_string(pages[0], lang="por")

    processo = extrair_campo(r"N[úu]mero Processo[:\s]+([\d./-]+)", texto)
    nome = extrair_campo(
        r"Interessado:\s*\d+\s*-\s*([A-ZÇÉÈÂÊÔÛÃÕÁÍÓÚ ]+?)\s+CPF/CNPJ", texto
    )
    endereco = extrair_campo(r"Endere[cç]o:\s*(.+)", texto)

    context = {
        "nome": nome,
        "processo": processo,
        "endereco": endereco,
        "data_parecer": datetime.now().strftime("%d de %B de %Y"),
    }

    nome_pdf = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(output_dir, f"{nome_pdf}.docx")

    doc = DocxTemplate(modelo_docx)
    doc.render(context)
    doc.save(output_path)

    return output_path

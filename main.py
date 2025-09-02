import re
import pytesseract
from pdf2image import convert_from_path
from docxtpl import DocxTemplate
from datetime import datetime
import locale

# --------- CONFIGURAÇÕES ----------
PDF_PATH = "entrada.pdf"
DOCX_MODEL = "modelo.docx"
DOCX_OUTPUT = "saida.docx"
# ----------------------------------

# Configurar locale para português (para nomes de meses)
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# 1️⃣ Extrair apenas a primeira página do PDF (OCR)
pages = convert_from_path(PDF_PATH, first_page=1, last_page=1)
texto = pytesseract.image_to_string(pages[0], lang="por")

print("=== TEXTO EXTRAÍDO DA PRIMEIRA PÁGINA ===")
print(texto[:2000])  # mostra só os primeiros 2000 caracteres


# Função auxiliar para regex
def extrair_campo(pattern, text, group=1):
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return match.group(group).strip() if match else ""


# 2️⃣ Extrair campos com regex

# Número do processo
processo = extrair_campo(r"N[úu]mero Processo[:\s]+([\d./-]+)", texto)

# Nome (para antes de "CPF/CNPJ")
nome = extrair_campo(
    r"Interessado:\s*\d+\s*-\s*([A-ZÇÉÈÂÊÔÛÃÕÁÍÓÚ ]+?)\s+CPF/CNPJ", texto
)

# Endereço
endereco = extrair_campo(r"Endere[cç]o:\s*(.+)", texto)

# 3️⃣ Montar contexto para preencher no modelo
context = {
    "nome": nome,
    "processo": processo,
    "endereco": endereco,
    "data_parecer": datetime.now().strftime("%d de %B de %Y"),
}

print("=== CONTEXT FINAL ===")
print(context)

# 4️⃣ Preencher modelo DOCX
doc = DocxTemplate(DOCX_MODEL)
doc.render(context)
doc.save(DOCX_OUTPUT)

print(f"✅ Documento gerado: {DOCX_OUTPUT}")

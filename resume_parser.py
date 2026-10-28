import io, re

def extract_resume_text(uploaded_file) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        uploaded_file.seek(0)
        return "\n".join(pages).strip()
    except Exception:
        pass
    try:
        import PyPDF2
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
        uploaded_file.seek(0)
        return text.strip()
    except Exception:
        pass
    uploaded_file.seek(0)
    raw = uploaded_file.read()
    text = re.sub(r'[^\x20-\x7E\n]', ' ', raw.decode('latin-1', errors='replace'))
    return re.sub(r' {2,}', ' ', text).strip()

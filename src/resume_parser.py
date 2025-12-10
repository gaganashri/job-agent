from pdfminer.high_level import extract_text

def pdf_to_text(path):
    try:
        text = extract_text(path)
        if not text:
            return "ERROR: No text extracted. The PDF might be scanned."
        text = " ".join(text.split())
        return text
    except Exception as e:
        return f"ERROR reading PDF: {e}"

if __name__ == "__main__":
    print("Testing resume extraction...")
    sample_path = "data/resumes/my_resume.pdf"
    print(pdf_to_text(sample_path)[:1500])

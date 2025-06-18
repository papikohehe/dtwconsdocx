import streamlit as st
from docx import Document
import re
from collections import Counter

def extract_line_numbers(doc):
    numbers = []
    for para in doc.paragraphs:
        text = para.text.strip()
        match = re.match(r'^L(\d{1,3})', text)
        if match:
            numbers.append(int(match.group(1)))
    return numbers

def analyze_line_numbers(numbers):
    if not numbers:
        return [], []
    unique = sorted(set(numbers))
    full_range = range(unique[0], unique[-1] + 1)
    missing = [n for n in full_range if n not in numbers]
    duplicates = [n for n, c in Counter(numbers).items() if c > 1]
    return missing, duplicates

def main():
    st.title("📄 Batch DOCX Line Number Checker")
    st.write("Upload one or more `.docx` files. Each file will be checked for missing or duplicate line numbers (L{number}).")

    uploaded_files = st.file_uploader("Upload DOCX files", type="docx", accept_multiple_files=True)

    if uploaded_files:
        summary = []

        for file in uploaded_files:
            doc = Document(file)
            numbers = extract_line_numbers(doc)
            missing, duplicates = analyze_line_numbers(numbers)

            summary.append({
                "Filename": file.name,
                "Total Lines": len(numbers),
                "Missing": ", ".join(f"L{n}" for n in missing) if missing else "None",
                "Duplicates": ", ".join(f"L{n}" for n in duplicates) if duplicates else "None"
            })

        st.subheader("🧾 Check Summary")
        st.table(summary)

if __name__ == "__main__":
    main()

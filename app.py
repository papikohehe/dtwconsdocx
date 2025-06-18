import streamlit as st
from docx import Document
import re
from io import BytesIO

def extract_line_numbers(doc):
    line_numbers = []
    for para in doc.paragraphs:
        match = re.match(r'^L(\d{1,3})', para.text.strip())
        if match:
            line_numbers.append(int(match.group(1)))
    return sorted(set(line_numbers))

def find_missing_numbers(line_numbers):
    missing = []
    if not line_numbers:
        return missing
    for expected in range(line_numbers[0], line_numbers[-1] + 1):
        if expected not in line_numbers:
            missing.append(expected)
    return missing

def insert_missing_lines(doc, missing_numbers):
    new_doc = Document()
    all_paragraphs = list(doc.paragraphs)
    current_idx = 0

    for i in range(len(all_paragraphs)):
        para = all_paragraphs[i]
        match = re.match(r'^L(\d{1,3})', para.text.strip())
        if match:
            current_line_num = int(match.group(1))
            while current_idx < len(missing_numbers) and missing_numbers[current_idx] < current_line_num:
                new_doc.add_paragraph(f"L{missing_numbers[current_idx]}: << Missing Line >>")
                current_idx += 1
        new_doc.add_paragraph(para.text)

    # Add any missing at the end
    while current_idx < len(missing_numbers):
        new_doc.add_paragraph(f"L{missing_numbers[current_idx]}: << Missing Line >>")
        current_idx += 1

    return new_doc

def generate_download_link(doc):
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def main():
    st.title("📄 Line Number Checker & Auto-Fix for DOCX")
    st.write("Upload a `.docx` file. We'll check for missing `L{number}` lines and optionally auto-fix them.")

    uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

    if uploaded_file:
        doc = Document(uploaded_file)
        line_numbers = extract_line_numbers(doc)
        missing = find_missing_numbers(line_numbers)

        st.subheader("📋 Detected Line Numbers")
        st.write([f"L{n}" for n in line_numbers])

        if missing:
            st.subheader("❌ Missing Line Numbers")
            st.error(", ".join([f"L{m}" for m in missing]))

            if st.button("🛠️ Auto-insert missing lines"):
                fixed_doc = insert_missing_lines(doc, missing)
                st.success("Missing lines inserted as placeholders.")

                buffer = generate_download_link(fixed_doc)
                st.download_button(
                    label="📥 Download Fixed DOCX",
                    data=buffer,
                    file_name="fixed_document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            st.success("✅ All line numbers are present and in sequence!")

if __name__ == "__main__":
    main()

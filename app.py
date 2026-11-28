import re
import json
import pandas as pd
import streamlit as st
from src.document_processing.pdf_extractor import extract_text_from_pdf
from src.extraction.info_extractor import extract_info

st.set_page_config(page_title="Intelligent Document Analyzer", layout="wide")
st.title("📄 Intelligent Document Analyzer")

files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
if not files:
    st.info("Upload one or more PDFs to begin.")
    st.stop()

st.sidebar.metric("Documents", len(files))
st.sidebar.metric("Total size (MB)", round(sum(f.size for f in files) / 1024**2, 2))

for f in files:
    result = extract_text_from_pdf(f.getvalue())
    info = extract_info(result["pages"], result["links_by_page"])

    st.header(f.name)
    c1, c2, c3 = st.columns(3)
    c1.metric("Pages", result["total_pages"])
    c2.metric("Words", result["total_words"])
    c3.metric("Size (KB)", round(f.size / 1024, 2))

    tabs = st.tabs(["Dates", "Deadlines", "Eligibility", "Contact", "Application",
                    "Fees/Stipend/Duration", "Tasks", "Instructions", "Links", "Full text"])

   

    def show(items):
        if not items:
            st.caption("Nothing found.")
        for it in items:
            parts = re.split(r"\s(?=\d{1,2}\.\s+[A-Z])|\s*●\s*", it["text"])
            parts = [p.strip() for p in parts if p.strip()]
            parts = [re.sub(r"^(\d+)\.", r"\1\\.", p) for p in parts]  # keep "1." as literal text
            body = "\n".join(f"- {p}" for p in parts)
            st.markdown(f"{body}\n\n<small>📍 Page {it['page']}</small>", unsafe_allow_html=True)

    with tabs[0]: show(info["Dates"])
    with tabs[1]: show(info["Deadlines"])
    with tabs[2]: show(info["Eligibility"])
    with tabs[3]:
        st.subheader("Emails"); show(info["Emails"])
        st.subheader("Phones"); show(info["Phones"])
    with tabs[4]: show(info["Application"])
    with tabs[5]:
        for k in ["Fees", "Stipend", "Duration"]:
            st.subheader(k); show(info[k])
    with tabs[6]: show(info["Tasks"])
    with tabs[7]: show(info["Instructions"])
    with tabs[8]:
        for it in info["Links"]:
            st.markdown(f"- [{it['text']}]({it['text']}) (page {it['page']})")
    with tabs[9]:
        for p in result["pages"]:
            st.subheader(f"Page {p['page_number']}")
            st.text(p["text"])

    full_text = "\n\n".join(f"--- Page {p['page_number']} ---\n{p['text']}" for p in result["pages"])
    d1, d2 = st.columns(2)
    d1.download_button("⬇ Full text (.txt)", full_text, f"{f.name}.txt", key=f"t{f.name}")
    d2.download_button("⬇ Structured info (.json)", json.dumps(info, indent=2),
                       f"{f.name}.json", key=f"j{f.name}")
    st.divider()

import streamlit as st

st.set_page_config(
    page_title="Intelligent Document Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Intelligent Document Analyzer")

st.write(
    "Upload PDF documents to extract, classify, "
    "summarize and analyze their content."
)

st.divider()

st.sidebar.title("Navigation")
st.sidebar.info("Document Analyzer | Day 2")

st.header("Upload Your Documents")

uploaded_files = st.file_uploader(
    "Choose PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(
        f"{len(uploaded_files)} document(s) uploaded successfully!"
    )

    total_size = 0

    for index, uploaded_file in enumerate(uploaded_files):
        st.subheader(f"{index + 1}. {uploaded_file.name}")

        file_size = uploaded_file.size
        total_size += file_size

        col1, col2 = st.columns(2)

        with col1:
            st.metric("File Size", f"{file_size / 1024:.2f} KB")

        with col2:
            st.metric("File Type", "PDF")

    st.divider()
    st.subheader("Upload Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Documents", len(uploaded_files))

    with col2:
        st.metric("Total Size", f"{total_size / (1024 * 1024):.2f} MB")

else:
    st.info("Please upload PDF documents to get started.")

st.divider()

st.caption("Intelligent Document Analyzer | AI + ML + NLP")

import pymupdf

def extract_text_from_pdf(file_bytes):
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    pages, total_words, links_by_page = [], 0, {}
    try:
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text")
            wc = len(text.split())
            total_words += wc
            pages.append({"page_number": i, "text": text, "word_count": wc})
            uris = [l["uri"] for l in page.get_links() if l.get("uri")]
            if uris:
                links_by_page[i] = uris
        return {"total_pages": len(doc), "total_words": total_words,
                "pages": pages, "links_by_page": links_by_page}
    finally:
        doc.close()
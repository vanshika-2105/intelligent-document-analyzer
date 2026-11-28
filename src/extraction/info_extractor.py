import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3,5}\)?[\s-]?)\d{3,5}[\s-]?\d{3,5}")
URL = re.compile(r"https?://[^\s<>\")\]]+|www\.[^\s<>\")\]]+")
DATE = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?,?\s+\d{2,4}\b"
    r"|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{2,4}\b",
    re.I,
)

KEYWORDS = {
    "Deadlines": ["deadline", "last date", "due", "submit by", "closing", "apply before"],
    "Eligibility": ["eligib", "qualification", "must be", "should be", "required", "criteria", "year student", "cgpa"],
    "Fees": ["fee", "registration charge", "payment", "cost"],
    "Stipend": ["stipend", "salary", "compensation", "reward", "prize", "certificate"],
    "Duration": ["duration", "weeks", "months", "period", "schedule"],
    "Tasks": ["task", "responsibilit", "assignment", "project", "deliverable"],
    "Instructions": ["instruction", "note:", "important", "mandatory", "do not", "must"],
    "Application": ["apply", "application", "registration", "register", "google form", "submit"],
}


def split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?:;])\s+|•|\u2022", text) if len(s.strip()) > 3]


def extract_info(pages, links_by_page=None):
    """pages: list of {'page_number','text'}; returns dict of categories -> list of {page, text}."""
    info = {k: [] for k in ["Dates", "Emails", "Phones", "Links", *KEYWORDS]}
    seen = {k: set() for k in info}

    def add(cat, page, text):
        key = text.lower()
        if key not in seen[cat]:
            seen[cat].add(key)
            info[cat].append({"page": page, "text": text})

    for p in pages:
        n, text = p["page_number"], p["text"]
        for m in EMAIL.findall(text):
            add("Emails", n, m)
        for m in URL.findall(text):
            add("Links", n, m.rstrip(".,;"))
        for m in PHONE.findall(text):
            digits = re.sub(r"\D", "", m)
            if 10 <= len(digits) <= 13:
                add("Phones", n, m.strip())

        for sent in split_sentences(text):
            if DATE.search(sent):
                add("Dates", n, sent)
            low = sent.lower()
            for cat, words in KEYWORDS.items():
                if any(w in low for w in words):
                    add(cat, n, sent)

    for page_no, urls in (links_by_page or {}).items():
        for u in urls:
            add("Links", page_no, u)
    return info
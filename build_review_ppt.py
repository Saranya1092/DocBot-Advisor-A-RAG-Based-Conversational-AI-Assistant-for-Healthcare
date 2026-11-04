"""Build the DocBot Advisor Review-2 presentation (18 slides)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

W, H = 13.333, 7.5
TOTAL = 18

NAVY = RGBColor(0x0B, 0x2D, 0x40)
TEAL = RGBColor(0x0E, 0x7C, 0x7B)
TEAL_SOFT = RGBColor(0x1A, 0x9B, 0x98)
MINT = RGBColor(0xE6, 0xF3, 0xF2)
MINT2 = RGBColor(0xF3, 0xF8, 0xF8)
CREAM = RGBColor(0xF7, 0xF5, 0xF0)
GOLD = RGBColor(0xC4, 0x95, 0x3A)
INK = RGBColor(0x1C, 0x28, 0x33)
MUTED = RGBColor(0x5A, 0x6B, 0x76)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xD3, 0xE3, 0xE1)
GREEN = RGBColor(0x1B, 0x7A, 0x4E)
GREEN_BG = RGBColor(0xE5, 0xF4, 0xEB)
CORAL = RGBColor(0xA3, 0x45, 0x42)


def rgb_hex(shape_fill):
    return shape_fill


def rect(slide, l, t, w, h, fill, line_color=None, line_pt=1):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
        sh.line.width = Pt(line_pt)
    sh.shadow.inherit = False
    return sh


def rrect(slide, l, t, w, h, fill, line_color=None, line_pt=1, radius=0.08):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
        sh.line.width = Pt(line_pt)
    try:
        sh.adjustments[0] = radius
    except Exception:
        pass
    sh.shadow.inherit = False
    return sh


def _anchor(tf, anchor):
    mapping = {"t": "t", "ctr": "ctr", "b": "b"}
    tf._txBody.bodyPr.set("anchor", mapping.get(anchor, "t"))


def write(slide, l, t, w, h, lines, anchor="t"):
    """lines: list of (text, size, bold, color, align, before, after)."""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    _anchor(tf, anchor)
    for i, item in enumerate(lines):
        text, size, bold, color = item[0], item[1], item[2], item[3]
        align = item[4] if len(item) > 4 else PP_ALIGN.LEFT
        before = item[5] if len(item) > 5 else 0
        after = item[6] if len(item) > 6 else 0
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(before)
        p.space_after = Pt(after)
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = "Calibri"
    return box


def chrome(slide, section, title, page):
    rect(slide, 0, 0, W, 0.08, TEAL)
    rect(slide, 0, 0.08, W, 1.08, NAVY)
    write(slide, 0.48, 0.16, 10, 0.28, [(section.upper(), 12, True, TEAL_SOFT)])
    write(slide, 0.46, 0.40, 12.2, 0.62, [(title, 28, True, WHITE)])
    rect(slide, 0, 7.18, W, 0.32, NAVY)
    write(
        slide, 0.42, 7.20, 9.2, 0.26,
        [("DocBot Advisor   |   SARANYA K   |   22MIS0195", 12, False, WHITE)],
        anchor="ctr",
    )
    write(
        slide, 10.6, 7.20, 2.3, 0.26,
        [(f"{page}   /   {TOTAL}", 12, False, WHITE, PP_ALIGN.RIGHT)],
        anchor="ctr",
    )


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def style_cell(cell, text, fill, color, size=13, bold=False, align=PP_ALIGN.LEFT):
    cell.text = ""
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Inches(0.1)
    cell.margin_right = Inches(0.08)
    cell.margin_top = Inches(0.04)
    cell.margin_bottom = Inches(0.04)
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for edge in ("lnL", "lnR", "lnT", "lnB"):
        ln = etree.SubElement(tcPr, qn(f"a:{edge}"))
        ln.set("w", "6350")
        sf = etree.SubElement(ln, qn("a:solidFill"))
        c = etree.SubElement(sf, qn("a:srgbClr"))
        c.set("val", "D3E3E1")


def build():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = "DocBot Advisor — Review 2"
    prs.core_properties.author = "SARANYA K"
    prs.core_properties.subject = "SWE3004 Software Design and Development Project"
    prs.core_properties.category = "Review 2"

    # ----- 1 Title -----
    s = blank(prs)
    rect(s, 0, 0, W, H, NAVY)
    rect(s, 0, 0, 0.16, H, GOLD)
    rect(s, 0, 7.32, W, 0.18, TEAL)
    write(s, 0.7, 0.42, 11, 0.3, [
        ("SCHOOL OF COMPUTER SCIENCE ENGINEERING AND INFORMATION SYSTEMS", 13, True, TEAL_SOFT)
    ])
    write(s, 0.7, 0.78, 11, 0.32, [
        ("SWE3004   ·   Software Design and Development Project   ·   Review 2", 16, False, RGBColor(0xC5, 0xD4, 0xDC))
    ])
    write(s, 0.7, 1.85, 12, 0.95, [("DocBot Advisor", 54, True, WHITE)])
    write(s, 0.7, 2.85, 11.2, 0.85, [
        ("A retrieval-augmented generation assistant for healthcare", 22, False, RGBColor(0xE4, 0xEE, 0xF0)),
        ("document question-answering", 22, False, RGBColor(0xE4, 0xEE, 0xF0), PP_ALIGN.LEFT, 2, 0),
    ])
    rect(s, 0.72, 3.85, 2.1, 0.055, GOLD)
    write(s, 0.7, 4.15, 6, 0.45, [("SARANYA K", 28, True, WHITE)])
    write(s, 0.7, 4.62, 6, 0.32, [("Register Number  22MIS0195", 16, False, RGBColor(0xC5, 0xD4, 0xDC))])
    write(s, 7.6, 4.15, 5, 0.28, [("Under the guidance of", 14, False, TEAL_SOFT)])
    write(s, 7.6, 4.46, 5.2, 0.38, [("Prof. Dr. Chandrasegar T", 22, True, WHITE)])
    write(s, 7.6, 4.92, 5.2, 0.3, [("Assistant Professor, Senior Grade 2", 15, False, RGBColor(0xC5, 0xD4, 0xDC))])
    write(s, 0.7, 6.55, 11.5, 0.4, [
        ("Department of Software and Systems Engineering     ·     Fall Semester 2026–27", 15, False, RGBColor(0xB7, 0xC8, 0xD0))
    ])
    notes(s, "Open with the project name and the one-line purpose: answers come only from the clinic’s own documents, not from a general chatbot.")

    # ----- 2 Agenda -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Overview", "Agenda", 2)
    items = [
        ("01", "Problem and objectives", "Why rural clinics need a grounded assistant"),
        ("02", "Literature gap", "What existing clinical ML does not solve"),
        ("03", "Proposed RAG system", "From documents to a checked answer"),
        ("04", "Architecture and modules", "Five layers and four Python modules"),
        ("05", "Safety and technology", "Guardrails, free models, and local index"),
        ("06", "Testing and next steps", "Eight checks, results, and future work"),
    ]
    for i, (num, title, sub) in enumerate(items):
        col, row = i % 2, i // 2
        x = 0.48 + col * 6.4
        y = 1.48 + row * 1.78
        rrect(s, x, y, 6.1, 1.58, WHITE, LINE, 1, 0.08)
        rect(s, x, y, 0.1, 1.58, TEAL)
        write(s, x + 0.35, y + 0.28, 1.1, 0.55, [(num, 26, True, TEAL)])
        write(s, x + 1.55, y + 0.32, 4.2, 0.45, [(title, 20, True, INK)])
        write(s, x + 1.55, y + 0.85, 4.2, 0.45, [(sub, 15, False, MUTED)])
    notes(s, "Tell the panel the talk follows the review rubric: problem, design, implementation, and testing. About one minute per remaining slide.")

    # ----- 3 Why -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Introduction", "Why DocBot Advisor", 3)
    rrect(s, 0.45, 1.45, 7.35, 5.4, WHITE, LINE, 1, 0.06)
    write(s, 0.75, 1.7, 6.8, 1.5, [
        ("Clinical answers must come from the clinic’s own documents.", 24, True, NAVY),
    ])
    write(s, 0.75, 3.35, 6.75, 3.1, [
        ("Primary health centres and rural clinics are often staffed by community health workers, ASHAs, ANMs, and junior officers. Protocols, drug manuals, and advisories sit in long PDFs, Word files, websites, and training videos.", 16, False, INK, PP_ALIGN.LEFT, 0, 10),
        ("A general chatbot can sound confident and still invent a dose or a contraindication. DocBot Advisor retrieves the relevant passage first, then answers only from that passage.", 16, False, INK, PP_ALIGN.LEFT, 8, 0),
    ])
    points = [
        ("Scattered sources", "PDF, DOCX, web pages, and video transcripts"),
        ("No time to search", "Staff cannot flip manuals during a consultation"),
        ("Hallucination risk", "Ungrounded models fabricate clinical facts"),
        ("No audit trail", "Earlier chat tools do not keep a reviewable log"),
    ]
    for i, (t, d) in enumerate(points):
        y = 1.45 + i * 1.38
        rrect(s, 8.05, y, 4.8, 1.25, WHITE, LINE, 1, 0.1)
        rect(s, 8.05, y, 0.1, 1.25, GOLD)
        write(s, 8.4, y + 0.18, 4.2, 0.4, [(t, 16, True, NAVY)])
        write(s, 8.4, y + 0.62, 4.2, 0.45, [(d, 13, False, MUTED)])
    notes(s, "Stress the user: a health worker with many patients and paper manuals. The product is decision support, not a replacement for a doctor.")

    # ----- 4 Problem -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Problem", "Problem Statement", 4)
    problems = [
        ("01", "Knowledge is scattered", "Treatment steps, paediatric doses, and drug notes live in disconnected files and links."),
        ("02", "Look-up is too slow", "A waiting queue leaves no time to search multi-page manuals by hand."),
        ("03", "General AI is unsafe here", "Models that are not tied to a source can give non-local or invented advice."),
        ("04", "Cost and exposed keys", "Paid medical APIs are hard for a small clinic, and keys must not sit in the browser."),
        ("05", "Consultations are not recorded", "There is no standard export a senior doctor can review later."),
    ]
    for i, (n, t, d) in enumerate(problems):
        y = 1.40 + i * 1.10
        rrect(s, 0.45, y, 12.4, 1.00, WHITE, LINE, 1, 0.08)
        rrect(s, 0.62, y + 0.22, 0.7, 0.56, TEAL, radius=0.2)
        write(s, 0.62, y + 0.30, 0.7, 0.42, [(n, 14, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        write(s, 1.55, y + 0.12, 10.9, 0.38, [(t, 18, True, NAVY)])
        write(s, 1.55, y + 0.50, 10.9, 0.38, [(d, 14, False, MUTED)])
    notes(s, "Read the five gaps quickly. End on the need: a zero-cost assistant that answers from local documents and keeps a log.")

    # ----- 5 Objectives -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Objectives", "What the System Must Do", 5)
    objs = [
        ("1", "Ingest many sources", "PDF, DOCX, medical web pages, and YouTube transcripts in one pipeline."),
        ("2", "Embed the text", "Split into overlapping chunks and encode them with BAAI/bge-small-en."),
        ("3", "Keep a local index", "Store vectors in ChromaDB so documents are not embedded again on restart."),
        ("4", "Answer at no model fee", "Call OpenRouter free models, including Ling 3.0 Santé."),
        ("5", "Refuse when unsure", "If the retrieved text does not support an answer, say so."),
        ("6", "Remember and export", "Keep the session dialogue and save it as a timestamped CSV."),
    ]
    for i, (n, t, d) in enumerate(objs):
        col, row = i % 3, i // 3
        x = 0.42 + col * 4.25
        y = 1.48 + row * 2.7
        rrect(s, x, y, 4.05, 2.48, WHITE, LINE, 1, 0.08)
        rrect(s, x + 0.22, y + 0.24, 0.58, 0.58, TEAL, radius=0.3)
        write(s, x + 0.22, y + 0.32, 0.58, 0.44, [(n, 18, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        write(s, x + 0.22, y + 1.02, 3.6, 0.5, [(t, 18, True, NAVY)])
        write(s, x + 0.22, y + 1.52, 3.6, 0.75, [(d, 14, False, MUTED)])
    notes(s, "These six objectives map directly to dataloader.py, llm.py, and app.py. Credential isolation is covered on the safety slide.")

    # ----- 6 Literature -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Literature", "What Existing Work Leaves Open", 6)
    write(s, 0.5, 1.38, 12.3, 0.4, [
        ("Fifteen surveyed papers focus on heart-disease and diabetes classifiers trained on structured tables.", 16, False, INK)
    ])
    findings = [
        ("They classify rows, not manuals", "Reported accuracy is often 85–92% on datasets such as UCI Heart Disease. They cannot read a protocol, a drug monograph, or a public-health bulletin."),
        ("They give a score, not an explanation", "A health worker cannot ask a follow-up about dose, contraindication, or the next triage step. The output is a label."),
        ("They go stale", "New circulars and local drug lists do not change a trained model. Accuracy also drops when clinic records are missing or noisy."),
    ]
    for i, (t, d) in enumerate(findings):
        y = 1.95 + i * 1.35
        rrect(s, 0.45, y, 12.4, 1.22, WHITE, LINE, 1, 0.08)
        rect(s, 0.45, y, 0.1, 1.22, TEAL)
        write(s, 0.8, y + 0.12, 11.7, 0.36, [(t, 18, True, NAVY)])
        write(s, 0.8, y + 0.52, 11.7, 0.58, [(d, 14, False, INK)])
    rrect(s, 0.45, 6.05, 12.4, 0.95, NAVY, radius=0.08)
    write(s, 0.7, 6.22, 11.9, 0.62, [
        ("DocBot Advisor does not train another classifier. It retrieves the clinic’s current text and answers from that text.", 16, True, WHITE)
    ], anchor="ctr")
    notes(s, "Do not walk through all 15 papers. State the shared limit, then the design choice: retrieval over retraining.")

    # ----- 7 Proposed system -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Proposed system", "Five-Step RAG Pipeline", 7)
    steps = [
        ("1", "Sources", "Clinical PDF, DOCX, web pages, YouTube links"),
        ("2", "Ingest", "PyMuPDF, Unstructured, web loader, transcripts"),
        ("3", "Embed", "1,000-character chunks, BGE-small-en"),
        ("4", "Retrieve", "ChromaDB, top 3 by cosine similarity"),
        ("5", "Answer", "Free LLM, safety prompt, CSV log"),
    ]
    card_w, pitch = 2.28, 2.58
    for i, (n, t, d) in enumerate(steps):
        x = 0.32 + i * pitch
        rrect(s, x, 1.7, card_w, 3.35, WHITE, LINE, 1, 0.08)
        rect(s, x, 1.7, card_w, 0.12, TEAL)
        rrect(s, x + 0.78, 2.05, 0.72, 0.72, TEAL, radius=0.4)
        write(s, x + 0.78, 2.18, 0.72, 0.5, [(n, 22, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        write(s, x + 0.12, 2.95, card_w - 0.24, 0.45, [(t, 18, True, NAVY, PP_ALIGN.CENTER)])
        write(s, x + 0.12, 3.5, card_w - 0.24, 1.25, [(d, 13, False, MUTED, PP_ALIGN.CENTER)])
        if i < 4:
            write(
                s, x + card_w, 3.0, pitch - card_w, 0.45,
                [("›", 20, True, TEAL, PP_ALIGN.CENTER)],
                anchor="ctr",
            )
    rrect(s, 0.45, 5.3, 12.4, 1.55, WHITE, LINE, 1, 0.06)
    write(s, 0.75, 5.5, 11.9, 0.4, [("Grounding rule", 16, True, TEAL)])
    write(s, 0.75, 5.95, 11.9, 0.7, [
        ("The model sees only the retrieved chunks. If they do not contain the answer, it must reply: “I’m sorry, I don’t have enough information to answer that.”", 16, False, INK)
    ])
    notes(s, "Walk left to right. Pause on step 5: refusal is a feature, not a failure.")

    # ----- 8 Architecture -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Architecture", "Five-Layer Design", 8)
    layers = [
        ("Presentation", "Streamlit", "Sidebar for model, chunk size, overlap, and top-k. Chat panel for the consultation."),
        ("Controller", "app.py", "Session state, Process Data, API-key check, and CSV export."),
        ("RAG engine", "dataloader + llm", "Loaders, splitter, retriever, conversation memory, and the medical prompt."),
        ("Storage", "ChromaDB", "384-dimension BGE vectors saved on disk in chromadb_store."),
        ("Inference", "OpenRouter", "Free models: Ling 3.0 Santé, Gemma 4 31B, Qwen, Nemotron, or the free router."),
    ]
    for i, (name, tag, detail) in enumerate(layers):
        y = 1.40 + i * 1.10
        rrect(s, 0.45, y, 12.4, 1.00, WHITE, LINE, 1, 0.08)
        rrect(s, 0.6, y + 0.18, 2.55, 0.64, NAVY if i % 2 == 0 else TEAL, radius=0.12)
        write(s, 0.7, y + 0.30, 2.35, 0.42, [(name, 15, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        write(s, 3.4, y + 0.12, 9.1, 0.34, [(tag, 15, True, NAVY)])
        write(s, 3.4, y + 0.48, 9.1, 0.4, [(detail, 14, False, INK)])
    notes(s, "Point out separation of concerns. UI never holds the API key. Retrieval and generation are different layers.")

    # ----- 9 Methodology -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Methodology", "Pipeline Settings", 9)
    rows = [
        ("Stage", "Method", "Setting used"),
        ("Ingestion", "PDF, DOCX, web, YouTube", "PyMuPDF, Unstructured, WebBaseLoader, transcripts"),
        ("Chunking", "Recursive character split", "1,000 characters, overlap 50 (user can change)"),
        ("Embedding", "BAAI/bge-small-en", "384 dimensions, cosine-normalised"),
        ("Index", "ChromaDB on disk", "Folder chromadb_store, reused across runs"),
        ("Retrieval", "Similarity search", "Top-k = 3 by default (range 1–10)"),
        ("Generation", "Conversational RAG chain", "OpenRouter free LLM, temperature 0.7"),
        ("Record", "Streamlit session", "Chat memory, CSV export, logs/docbot.log"),
    ]
    table_shape = s.shapes.add_table(8, 3, Inches(0.45), Inches(1.42), Inches(12.4), Inches(5.5))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(4.3)
    table.columns[2].width = Inches(5.9)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            if r == 0:
                style_cell(table.cell(r, c), val, NAVY, WHITE, 14, True)
            else:
                fill = WHITE if r % 2 else MINT
                style_cell(table.cell(r, c), val, fill, INK, 13, c == 0)
    notes(s, "If asked why 1,000 and overlap 50: short enough to stay on one topic, overlap so a dose table is not cut in half. Top-k 3 keeps the prompt focused.")

    # ----- 10 Use cases -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "UML", "Actors and Use Cases", 10)
    rrect(s, 0.42, 1.42, 3.7, 2.55, NAVY, radius=0.08)
    write(s, 0.62, 1.58, 3.3, 0.35, [("Clinic staff", 18, True, WHITE)])
    write(s, 0.62, 2.1, 3.3, 1.6, [
        ("Health worker or junior officer. Uploads sources, asks questions, reads the answer, and downloads the chat.", 14, False, RGBColor(0xE4, 0xEE, 0xF0))
    ])
    rrect(s, 0.42, 4.15, 3.7, 2.7, TEAL, radius=0.08)
    write(s, 0.62, 4.32, 3.3, 0.35, [("Clinic admin", 18, True, WHITE)])
    write(s, 0.62, 4.85, 3.3, 1.7, [
        ("Senior doctor. Sets chunk size, overlap, top-k, and the free model. Reviews exported chats and the log file.", 14, False, WHITE)
    ])
    cases = [
        ("UC01", "Upload PDF or DOCX", "Staff"),
        ("UC02", "Add a website or YouTube link", "Staff"),
        ("UC03", "Process and index the sources", "Staff"),
        ("UC04", "Ask a question in plain language", "Staff"),
        ("UC05", "Receive a grounded answer", "Staff"),
        ("UC06", "Download the chat as CSV", "Staff / Admin"),
        ("UC07", "Set model and retrieval settings", "Admin"),
        ("UC08", "Inspect logs/docbot.log", "Admin"),
    ]
    tbl = s.shapes.add_table(9, 3, Inches(4.35), Inches(1.42), Inches(8.5), Inches(5.45)).table
    tbl.columns[0].width = Inches(1.3)
    tbl.columns[1].width = Inches(5.15)
    tbl.columns[2].width = Inches(2.05)
    headers = ("ID", "Use case", "Actor")
    for c, h in enumerate(headers):
        style_cell(tbl.cell(0, c), h, NAVY, WHITE, 13, True)
    for i, (a, b, c) in enumerate(cases, start=1):
        fill = WHITE if i % 2 else MINT
        style_cell(tbl.cell(i, 0), a, fill, TEAL, 12, True)
        style_cell(tbl.cell(i, 1), b, fill, INK, 13, False)
        style_cell(tbl.cell(i, 2), c, fill, INK, 12, False)
    notes(s, "Two actors only. Staff does the consultation. Admin owns configuration and audit.")

    # ----- 11 Modules -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Implementation", "Four Modules", 11)
    mods = [
        ("app.py", "Orchestration", [
            "Loads the key from the .env file",
            "Runs ingestion, then builds the QA chain",
            "Shows the chat and writes the CSV",
        ]),
        ("dataloader.py", "Ingestion", [
            "PDF via PyMuPDFLoader",
            "DOCX via Unstructured",
            "Web pages and YouTube transcripts",
        ]),
        ("llm.py", "RAG chain", [
            "Splits, embeds, and stores in Chroma",
            "Retrieves top-k chunks",
            "Applies the safety prompt and memory",
        ]),
        ("streamlitui.py", "Interface", [
            "Free-model selector and chunk sliders",
            "Multi-file upload and URL boxes",
            "Full-width chat layout",
        ]),
    ]
    for i, (fname, role, bullets) in enumerate(mods):
        col, row = i % 2, i // 2
        x = 0.42 + col * 6.45
        y = 1.45 + row * 2.75
        rrect(s, x, y, 6.2, 2.55, WHITE, LINE, 1, 0.08)
        rect(s, x, y, 6.2, 0.7, NAVY)
        write(s, x + 0.25, y + 0.12, 3.6, 0.48, [(fname, 20, True, WHITE)], anchor="ctr")
        write(s, x + 3.5, y + 0.16, 2.45, 0.42, [(role, 14, True, GOLD, PP_ALIGN.RIGHT)], anchor="ctr")
        lines = []
        for b in bullets:
            lines.append(("•   " + b, 15, False, INK, PP_ALIGN.LEFT, 2, 2))
        write(s, x + 0.3, y + 0.9, 5.6, 1.45, lines)
    notes(s, "If asked about code quality: each file has one job. app.py does not parse PDFs. llm.py does not draw the UI.")

    # ----- 12 Stack -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Implementation", "Technology Choices", 12)
    groups = [
        ("Application", [
            ("Interface", "Streamlit 1.65"),
            ("Language", "Python 3.10"),
            ("Orchestration", "LangChain 1.4"),
            ("Tables and logs", "pandas, logging"),
        ]),
        ("Retrieval", [
            ("Embeddings", "BAAI/bge-small-en"),
            ("Vector size", "384, normalised"),
            ("Vector store", "ChromaDB 1.5.9"),
            ("Split", "1,000 / overlap 50"),
        ]),
        ("Models and access", [
            ("Gateway", "OpenRouter free tier"),
            ("Clinical model", "Ling 3.0 Santé"),
            ("Also available", "Gemma 4, Qwen, Nemotron"),
            ("Keys", ".env via python-dotenv"),
        ]),
    ]
    for i, (title, pairs) in enumerate(groups):
        x = 0.4 + i * 4.28
        rrect(s, x, 1.45, 4.08, 4.15, WHITE, LINE, 1, 0.08)
        rect(s, x, 1.45, 4.08, 0.62, TEAL)
        write(s, x + 0.15, 1.55, 3.78, 0.42, [(title, 18, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        for j, (k, v) in enumerate(pairs):
            y = 2.28 + j * 0.75
            write(s, x + 0.25, y, 3.6, 0.28, [(k, 12, True, MUTED)])
            write(s, x + 0.25, y + 0.26, 3.6, 0.32, [(v, 16, True, NAVY)])
    rrect(s, 0.4, 5.8, 12.5, 1.15, NAVY, radius=0.08)
    write(s, 0.65, 5.98, 12.0, 0.8, [
        ("Runs on a modest PC: 4 GB RAM minimum, 8 GB recommended. The index stays on disk. Only the final answer call needs the network.", 16, False, WHITE)
    ], anchor="ctr")
    notes(s, "Highlight two constraints: free inference, and a local index so the clinic does not re-embed on every launch.")

    # ----- 13 Safety -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Safety", "Guardrails, Keys, and Audit", 13)
    cards = [
        ("Answer only from context", "The system prompt forbids advice that is not in the retrieved chunks. Missing context produces a fixed refusal, not a guess."),
        ("Key stays on the server side", "OPENROUTER_API_KEY is read from .env. The sidebar has no password box, so the key is not typed into the page."),
        ("Every consult can be reviewed", "The session is kept in ConversationBufferMemory and saved under chat_exports as a timestamped CSV. Events go to logs/docbot.log."),
    ]
    for i, (t, d) in enumerate(cards):
        x = 0.4 + i * 4.28
        rrect(s, x, 1.45, 4.08, 3.15, WHITE, LINE, 1, 0.08)
        rect(s, x, 1.45, 4.08, 0.1, GOLD)
        write(s, x + 0.22, 1.75, 3.65, 0.9, [(t, 18, True, NAVY)])
        write(s, x + 0.22, 2.75, 3.65, 1.55, [(d, 14, False, INK)])
    rrect(s, 0.4, 4.85, 12.5, 2.05, WHITE, LINE, 1, 0.06)
    write(s, 0.65, 5.05, 12.0, 0.35, [("Refusal the model must use", 14, True, TEAL)])
    write(s, 0.65, 5.5, 12.0, 1.1, [
        ("“I’m sorry, I don’t have enough information to answer that.”", 22, True, NAVY)
    ])
    notes(s, "Quote the refusal line. Then say the key never appears in the Streamlit sidebar. Then mention the CSV as the medico-legal record.")

    # ----- 14 Testing -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Testing", "Verification Results", 14)
    tests = [
        ("ID", "What was checked", "Result"),
        ("TC01", "PDF and DOCX load into documents", "Pass"),
        ("TC02", "Standard and short YouTube links", "Pass"),
        ("TC03", "BGE vector is 384-d and normalised", "Pass"),
        ("TC04", "ChromaDB persists and is reused", "Pass"),
        ("TC05", "Malaria query returns ACT from the guideline", "Pass"),
        ("TC06", "Brain-surgery question is refused", "Pass"),
        ("TC07", "API key loads from .env only", "Pass"),
        ("TC08", "Chat exports to a timestamped CSV", "Pass"),
    ]
    tbl = s.shapes.add_table(9, 3, Inches(0.45), Inches(1.40), Inches(12.4), Inches(5.55)).table
    tbl.columns[0].width = Inches(1.4)
    tbl.columns[1].width = Inches(8.7)
    tbl.columns[2].width = Inches(2.3)
    for r, row in enumerate(tests):
        for c, val in enumerate(row):
            if r == 0:
                style_cell(tbl.cell(r, c), val, NAVY, WHITE, 14, True, PP_ALIGN.LEFT if c == 1 else PP_ALIGN.CENTER)
            else:
                fill = WHITE if r % 2 else MINT
                color = GREEN if c == 2 else (TEAL if c == 0 else INK)
                al = PP_ALIGN.LEFT if c == 1 else PP_ALIGN.CENTER
                style_cell(tbl.cell(r, c), val, GREEN_BG if c == 2 else fill, color, 14, c != 1, al)
    notes(s, "Call out TC05 and TC06 as the pair that matters: a real answer when the document has it, and a refusal when it does not.")

    # ----- 15 Demo -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Demonstration", "One Consultation", 15)
    flow = [
        ("1", "Set", "Pick a free model. Leave chunk size 1,000, overlap 50, top-k 3."),
        ("2", "Add sources", "Upload the protocol, or paste a page URL or a YouTube link."),
        ("3", "Index", "Process Data builds the Chroma store once."),
        ("4", "Ask", "Type the question in the chat box."),
        ("5", "Keep", "Download Chat as CSV for the senior doctor."),
    ]
    for i, (n, t, d) in enumerate(flow):
        y = 1.38 + i * 0.72
        rrect(s, 0.42, y, 7.35, 0.66, WHITE, LINE, 1, 0.1)
        rrect(s, 0.52, y + 0.12, 0.44, 0.42, TEAL, radius=0.3)
        write(s, 0.52, y + 0.16, 0.44, 0.34, [(n, 14, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        write(s, 1.12, y + 0.08, 1.7, 0.5, [(t, 15, True, NAVY)], anchor="ctr")
        write(s, 2.85, y + 0.1, 4.75, 0.48, [(d, 13, False, INK)], anchor="ctr")
    rrect(s, 7.95, 1.38, 4.9, 2.35, WHITE, LINE, 1, 0.08)
    rect(s, 7.95, 1.38, 0.1, 2.35, GREEN)
    write(s, 8.25, 1.52, 4.4, 0.3, [("Supported question", 13, True, GREEN)])
    write(s, 8.25, 1.9, 4.4, 1.55, [
        ("“First-line drug for uncomplicated P. falciparum?”", 14, True, NAVY, PP_ALIGN.LEFT, 0, 6),
        ("Answer cites artemisinin-based combination therapy from the indexed guideline.", 13, False, INK),
    ])
    rrect(s, 7.95, 3.9, 4.9, 2.35, WHITE, LINE, 1, 0.08)
    rect(s, 7.95, 3.9, 0.1, 2.35, CORAL)
    write(s, 8.25, 4.04, 4.4, 0.3, [("Unsupported question", 13, True, CORAL)])
    write(s, 8.25, 4.42, 4.4, 1.55, [
        ("“How do I perform brain tumour surgery?”", 14, True, NAVY, PP_ALIGN.LEFT, 0, 6),
        ("Refusal. The surgery steps are not in the uploaded context.", 13, False, INK),
    ])
    notes(s, "Demo live if the app is up: one in-document question, then one out-of-document question, then the CSV button.")

    # ----- 16 Outcomes -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Results", "What the Project Delivers", 16)
    wins = [
        ("Grounded answers", "Every reply is tied to retrieved clinic text, or it is refused."),
        ("Usable cost", "Inference stays on OpenRouter’s free models."),
        ("No repeat embedding", "ChromaDB keeps the index on disk between sessions."),
        ("Reviewable chats", "A timestamped CSV and a log file support later audit."),
        ("Checked behaviour", "Eight tests passed, covering loaders, retrieval, refusal, keys, and export."),
        ("Modular code", "Ingestion, chain, UI, and app control are separate files."),
    ]
    for i, (t, d) in enumerate(wins):
        col, row = i % 3, i // 3
        x = 0.42 + col * 4.25
        y = 1.45 + row * 2.15
        rrect(s, x, y, 4.05, 2.0, WHITE, LINE, 1, 0.08)
        rect(s, x, y, 4.05, 0.08, TEAL)
        write(s, x + 0.22, y + 0.28, 3.6, 0.5, [(t, 18, True, NAVY)])
        write(s, x + 0.22, y + 0.9, 3.6, 0.85, [(d, 14, False, INK)])
    notes(s, "This is the close of the results section. Six outcomes, each already shown in code or in a test.")

    # ----- 17 Scope and future -----
    s = blank(prs)
    rect(s, 0, 0, W, H, MINT2)
    chrome(s, "Scope", "Limits and Next Steps", 17)
    write(s, 0.48, 1.38, 6, 0.35, [("Outside this build", 16, True, MUTED)])
    limits = [
        "Does not replace a licensed doctor or issue a prescription.",
        "Does not read ECG, pulse-oximeter, or DICOM images.",
        "Does not diagnose from an X-ray or MRI.",
    ]
    for i, text in enumerate(limits):
        y = 1.85 + i * 1.62
        rrect(s, 0.45, y, 6.15, 1.48, WHITE, LINE, 1, 0.1)
        write(s, 0.7, y + 0.45, 5.7, 0.6, [(text, 15, False, INK)], anchor="ctr")
    write(s, 6.95, 1.38, 6, 0.35, [("Planned next", 16, True, MUTED)])
    futures = [
        ("Voice", "Speak a question and hear the answer, for low-literacy use."),
        ("Local languages", "Tamil, Hindi, Telugu, and Bengali replies."),
        ("Offline model", "Ollama fallback when the clinic network drops."),
        ("EHR export", "Map the CSV log toward HL7 / FHIR."),
    ]
    for i, (t, d) in enumerate(futures):
        y = 1.85 + i * 1.22
        rrect(s, 6.9, y, 5.95, 1.1, WHITE, LINE, 1, 0.1)
        write(s, 7.15, y + 0.1, 5.5, 0.32, [(t, 15, True, NAVY)])
        write(s, 7.15, y + 0.46, 5.5, 0.5, [(d, 13, False, MUTED)])
    notes(s, "Be explicit: this version is document QA. Voice, translation, offline LLM, and FHIR are the next review, not claims about the current demo.")

    # ----- 18 Close -----
    s = blank(prs)
    rect(s, 0, 0, W, H, NAVY)
    rect(s, 0, 0, 0.16, H, GOLD)
    rect(s, 0, 7.32, W, 0.18, TEAL)
    write(s, 0.7, 0.4, 11, 0.3, [("CONCLUSION", 14, True, TEAL_SOFT)])
    write(s, 0.7, 0.8, 12, 0.7, [("DocBot Advisor is ready for review", 32, True, WHITE)])
    points = [
        ("It answers from the clinic’s own PDF, Word, web, and video sources.",),
        ("BGE embeddings and a persistent Chroma index keep retrieval local and repeatable.",),
        ("Free OpenRouter models, a refusal prompt, and a hidden API key keep cost and risk down.",),
        ("Eight tests passed, including a correct malaria answer and a correct refusal.",),
    ]
    for i, (text,) in enumerate(points):
        y = 1.85 + i * 0.85
        rrect(s, 0.7, y, 0.5, 0.5, TEAL, radius=0.3)
        write(s, 0.7, y + 0.06, 0.5, 0.4, [(str(i + 1), 16, True, WHITE, PP_ALIGN.CENTER)], anchor="ctr")
        write(s, 1.45, y + 0.05, 10.8, 0.45, [(text, 18, False, WHITE)], anchor="ctr")
    rect(s, 0.72, 5.4, 2.0, 0.05, GOLD)
    write(s, 0.7, 5.6, 8, 0.45, [("Thank you", 28, True, WHITE)])
    write(s, 0.7, 6.15, 10, 0.35, [("SARANYA K   ·   22MIS0195   ·   Guide: Prof. Dr. Chandrasegar T", 15, False, RGBColor(0xC5, 0xD4, 0xDC))])
    write(s, 0.7, 6.55, 8, 0.35, [("Questions", 16, True, GOLD)])
    notes(s, "Stop after the four lines. Invite questions on the refusal case, the free models, and what is deliberately out of scope.")

    out = r"D:\10CC project\Saranya 22MIS0195\DOCBOT RAG PROJECT1\DocBot_Advisor_Review2.pptx"
    prs.save(out)
    print(out)
    print("slides", len(prs.slides))


if __name__ == "__main__":
    build()

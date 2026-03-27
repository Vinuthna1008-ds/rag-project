"""
states/rag_state.py
Central state — manages uploads, chat, and backend calls.
"""

import os
import shutil
import reflex as rx
from typing import List
from pydantic import BaseModel

from backend.rag import ingest, get_answer, reset_session as backend_reset


# ── PATH ─────────────────────────────────────────────
DOCUMENTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "documents"
)


# ── DATA MODEL ───────────────────────────────────────
class ChatItem(BaseModel):
    question: str
    answer: str
    sources: str


# ── STATE ────────────────────────────────────────────
class ChatState(rx.State):

    # ── Chat ─────────────────────────────────────────
    question: str = ""
    history: List[ChatItem] = []
    is_loading: bool = False
    error_msg: str = ""

    # ── Upload ───────────────────────────────────────
    uploaded_files: List[str] = []
    ingest_status: str = ""
    is_uploading: bool = False
    ingest_done: bool = False

    # ── INPUT ────────────────────────────────────────
    def set_question(self, value: str):
        self.question = value

    # ── FILE UPLOAD ──────────────────────────────────
    async def handle_upload(self, files: List[rx.UploadFile]):

        if not files:
            self.error_msg = "No files selected."
            return

        os.makedirs(DOCUMENTS_DIR, exist_ok=True)

        # Reset states
        self.error_msg = ""
        self.ingest_done = False
        self.is_uploading = True
        self.ingest_status = f"💾 Saving {len(files)} file(s)…"
        yield

        saved_paths: List[str] = []

        # Save files
        for uf in files:
            try:
                data = await uf.read()
                dest = os.path.join(DOCUMENTS_DIR, uf.filename)

                with open(dest, "wb") as f:
                    f.write(data)

                saved_paths.append(dest)
                self.uploaded_files.append(uf.filename)

                self.ingest_status = f"💾 Saved {uf.filename}"
                yield

            except Exception as e:
                self.error_msg = f"❌ Upload failed: {str(e)}"
                self.is_uploading = False
                return

        # Ingest
        self.ingest_status = "⚙️ Building vector DB..."
        yield

        try:
            chunks = ingest(saved_paths)

            self.ingest_status = (
                f"✅ Done! {len(saved_paths)} file(s) → {chunks} chunks"
            )
            self.ingest_done = True

        except Exception as e:
            self.error_msg = f"❌ Ingest error: {str(e)}"
            self.ingest_status = ""

        finally:
            self.is_uploading = False

    # ── CLEAR INGEST STATE ───────────────────────────
    def clear_ingest_done(self):
        self.ingest_done = False
        self.ingest_status = ""
        self.error_msg = ""

    def clear_error(self):
        self.error_msg = ""
        self.ingest_status = ""
        self.is_uploading = False
        self.ingest_done = False

    # ── CHAT ─────────────────────────────────────────
    def ask(self):

        q = self.question.strip()

        if not q:
            return

        self.is_loading = True
        self.error_msg = ""
        self.question = ""
        yield

        try:
            result = get_answer(q)

            answer = result.get("answer", "No answer generated.")
            sources = result.get("sources", [])

            if isinstance(sources, list):
                sources = ", ".join([os.path.basename(s) for s in sources])
            else:
                sources = str(sources)

            new_item = ChatItem(
                question=q,
                answer=answer,
                sources=sources
            )

            self.history = self.history + [new_item]

        except Exception as e:
            self.error_msg = f"❌ {str(e)}"

        finally:
            self.is_loading = False

    # ── CLEAR CHAT ───────────────────────────────────
    def clear_history(self):
        self.history = []

    # ── RESET SESSION ────────────────────────────────
    def reset_session(self):

        # Reset backend
        backend_reset()

        # Clear documents folder
        if os.path.exists(DOCUMENTS_DIR):
            shutil.rmtree(DOCUMENTS_DIR)

        os.makedirs(DOCUMENTS_DIR, exist_ok=True)

        # Reset frontend state
        self.history = []
        self.uploaded_files = []
        self.ingest_status = ""
        self.error_msg = ""
        self.question = ""
        self.is_loading = False
        self.is_uploading = False
        self.ingest_done = False

        return rx.redirect("/")

    # ── DOWNLOAD CHAT (PDF) ──────────────────────────
    def download_chat(self):

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        os.makedirs("assets", exist_ok=True)
        file_path = "assets/chat_history.pdf"

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        elements = []

        for item in self.history:
            elements.append(Paragraph(f"<b>Question:</b> {item.question}", styles["Normal"]))
            elements.append(Spacer(1, 10))

            elements.append(Paragraph(f"<b>Answer:</b> {item.answer}", styles["Normal"]))
            elements.append(Spacer(1, 10))

            elements.append(Paragraph(f"<b>Sources:</b> {item.sources}", styles["Normal"]))
            elements.append(Spacer(1, 20))

        doc.build(elements)

        return rx.download("/chat_history.pdf")
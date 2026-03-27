"""pages/upload.py"""

import reflex as rx
import os

from components.navbar import navbar
from components.footer import footer
from states.rag_state import ChatState


# ── PATH SETUP ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "documents")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── PAGE ──────────────────────────────────────────
@rx.page(route="/upload")
def upload() -> rx.Component:
    return rx.vstack(

        navbar(),

        rx.vstack(

            rx.heading("Upload Documents", size="7", text_align="center"),

            rx.text(
                "Supports PDF, TXT, and DOCX files. Upload multiple files at once.",
                color="gray",
                text_align="center",
            ),

            # ── UPLOAD AREA ─────────────────────────
            rx.cond(
                ~ChatState.is_uploading & ~ChatState.ingest_done,

                rx.vstack(

                    rx.upload(
                        rx.vstack(
                            rx.text("📂", size="8"),
                            rx.text("Drag & drop files or click to browse"),
                            rx.text(".pdf · .txt · .docx · .doc", size="2", color="gray"),
                            align="center",
                            padding="2em",
                        ),
                        id="upload_zone",
                        multiple=True,
                        border="2px dashed #6366f1",
                        border_radius="12px",
                        background="#f5f3ff",
                        width="100%",
                        max_width="600px",
                        cursor="pointer",
                        _hover={"background": "#ede9fe"},
                    ),

                    # Selected files preview
                    rx.foreach(
                        rx.selected_files("upload_zone"),
                        lambda f: rx.text(f"📎 {f}", size="2"),
                    ),

                    # Upload button
                    rx.button(
                        "Upload & Process",
                        color_scheme="violet",
                        width="100%",
                        max_width="600px",
                        on_click=ChatState.handle_upload(
                            rx.upload_files(upload_id="upload_zone")
                        ),
                    ),

                    spacing="4",
                    align="center",
                    width="100%",
                ),
            ),

            # ── LOADING ─────────────────────────────
            rx.cond(
                ChatState.is_uploading,

                rx.vstack(
                    rx.spinner(),
                    rx.text(ChatState.ingest_status, color="violet"),
                    rx.text("Please wait..."),
                    align="center",
                    spacing="3",
                    padding="2em",
                ),
            ),

            # ── SUCCESS ─────────────────────────────
            rx.cond(
                ChatState.ingest_done,

                rx.vstack(

                    rx.text("✅ Upload Successful!", color="green", size="5"),
                    rx.text(ChatState.ingest_status),

                    rx.link(
                        rx.button("Go to Chat →", color_scheme="violet"),
                        href="/chat",
                    ),

                    rx.button(
                        "Upload More",
                        on_click=ChatState.clear_ingest_done,
                        variant="soft",
                    ),

                    spacing="4",
                    align="center",
                ),
            ),

            # ── ERROR ──────────────────────────────
            rx.cond(
                ChatState.error_msg != "",
                rx.text(ChatState.error_msg, color="red"),
            ),

            # ── FILE LIST (REAL FILES FROM FOLDER) ─
            rx.vstack(
                rx.text("Uploaded Files:", font_weight="bold"),

                rx.foreach(
                    os.listdir(UPLOAD_DIR),
                    lambda f: rx.text(f"📄 {f}")
                ),

                width="100%",
                max_width="600px",
            ),

            spacing="5",
            padding="3em",
            align="center",
            width="100%",
            max_width="700px",
            margin="0 auto",
        ),

        footer(),
        spacing="0",
        min_height="100vh",
        background="#f8f9ff",
    )
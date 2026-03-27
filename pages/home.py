"""pages/home.py"""
import reflex as rx
from components.navbar import navbar
from components.hero import hero
from components.footer import footer


def features_section() -> rx.Component:
    cards = [
        ("📄", "PDF Support", "Upload and query any PDF document"),
        ("📝", "TXT Support", "Plain text files are fully supported"),
        ("📃", "DOCX Support", "Microsoft Word documents work seamlessly"),
        ("📂", "Directory Ingest", "Drop an entire folder — all files load automatically"),
        ("🧠", "Corrective RAG", "Automatic query rewriting for better retrieval"),
        ("💬", "Conversation Memory", "Follow-up questions just work"),
    ]
    return rx.vstack(
        rx.heading("Features", size="6", text_align="center"),
        rx.grid(
            *[
                rx.box(
                    rx.vstack(
                        rx.text(icon, size="6"),
                        rx.text(title, font_weight="700", size="3"),
                        rx.text(desc, color="gray", size="2", text_align="center"),
                        spacing="2",
                        align="center",
                    ),
                    padding="1.5em",
                    border="1px solid #e5e7eb",
                    border_radius="12px",
                    background="white",
                    box_shadow="0 1px 4px rgba(0,0,0,0.06)",
                )
                for icon, title, desc in cards
            ],
            columns="3",
            spacing="4",
            width="100%",
        ),
        spacing="6",
        padding_y="3em",
        width="100%",
        max_width="960px",
        margin="0 auto",
    )


@rx.page(route="/")
def home() -> rx.Component:
    return rx.vstack(
        navbar(),
        hero(),
        features_section(),
        footer(),
        spacing="0",
        min_height="100vh",
        background="linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%)",
    )
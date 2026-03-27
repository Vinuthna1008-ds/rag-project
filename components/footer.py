"""components/footer.py"""
import reflex as rx


def footer() -> rx.Component:
    return rx.box(
        rx.text(
            "RAG Chatbot — Built with Reflex + LangChain + ChromaDB + Groq",
            color="gray",
            text_align="center",
            size="2",
        ),
        padding="2em",
        width="100%",
        border_top="1px solid #eee",
    )
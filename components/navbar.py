"""components/navbar.py"""
import reflex as rx
from states.rag_state import ChatState


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("🤖 RAG Chatbot", size="5", color="white"),
                href="/",
                text_decoration="none",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link("Home", href="/", color="white", font_weight="500"),
                rx.link("Upload", href="/upload", color="white", font_weight="500"),
                rx.link("Chat", href="/chat", color="white", font_weight="500"),
                rx.link("History", href="/history", color="white", font_weight="500"),
                rx.button(
                    "Reset Session",
                    on_click=ChatState.reset_session,
                    size="2",
                    color_scheme="red",
                    variant="soft",
                ),
                spacing="5",
            ),
        ),
        background="linear-gradient(90deg, #1a1a2e 0%, #16213e 100%)",
        padding_x="2em",
        padding_y="1em",
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 8px rgba(0,0,0,0.3)",
    )
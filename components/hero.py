"""components/hero.py"""
import reflex as rx


def hero() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Chat with Your Documents",
            size="8",
            text_align="center",
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            background_clip="text",
            color="transparent",
        ),
        rx.text(
            "Upload PDF, TXT, or DOCX files — or entire directories — "
            "and ask questions powered by AI.",
            size="4",
            color="gray",
            text_align="center",
            max_width="600px",
        ),
        rx.hstack(
            rx.link(
                rx.button("Upload Documents", size="3", color_scheme="violet"),
                href="/upload",
            ),
            rx.link(
                rx.button("Start Chatting", size="3", variant="soft"),
                href="/chat",
            ),
            spacing="4",
        ),
        spacing="6",
        align="center",
        padding_y="5em",
    )
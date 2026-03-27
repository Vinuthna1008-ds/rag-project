"""
RAG_Project/rag_chatbot.py
Entry point — import all pages so Reflex discovers them.
"""

import reflex as rx

# Import pages to register routes
from pages.home import home
from pages.upload import upload
from pages.chat import chat
from pages.history import history

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="violet",
        radius="medium",
    ),
)
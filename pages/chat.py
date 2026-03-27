"""pages/chat.py"""

import reflex as rx
from components.navbar import navbar
from components.footer import footer
from states.rag_state import ChatState


# ── CHAT BUBBLE ─────────────────────────────────────
def chat_bubble(item) -> rx.Component:
    return rx.vstack(

        # ── USER MESSAGE (RIGHT) ─────────────────────
        rx.hstack(
            rx.spacer(),
            rx.box(
                rx.text(item.question, size="3", color="white"),
                background="linear-gradient(135deg, #667eea, #764ba2)",
                padding="0.8em 1.2em",
                border_radius="18px 18px 4px 18px",
                max_width="70%",
            ),
        ),

        # ── AI MESSAGE (LEFT) ────────────────────────
        rx.hstack(
            rx.box(
                rx.vstack(

                    # Answer
                    rx.text(item.answer, size="3"),

                    # ✅ FIXED: sources is STRING now
                    rx.cond(
                        item.sources != "",
                        rx.text(
                            "Sources: " + item.sources,
                            size="1",
                            color="gray"
                        ),
                        rx.text("")
                    ),

                    align="start",
                    spacing="2",
                ),
                background="white",
                padding="0.8em 1.2em",
                border_radius="18px 18px 18px 4px",
                border="1px solid #e5e7eb",
                max_width="70%",
                box_shadow="0 1px 4px rgba(0,0,0,0.06)",
            ),
            rx.spacer(),
        ),

        width="100%",
        spacing="3",
    )


# ── PAGE ───────────────────────────────────────────
@rx.page(route="/chat")
def chat() -> rx.Component:
    return rx.vstack(

        navbar(),

        rx.vstack(
            rx.heading("Chat", size="6"),

            # ── EMPTY STATE ─────────────────────────
            rx.cond(
                ChatState.history.length() == 0,
                rx.vstack(
                    rx.text("🤖", size="8"),
                    rx.text(
                        "Upload documents and ask me anything!",
                        color="gray",
                        size="4",
                    ),
                    rx.link(
                        rx.button("Upload Documents →"),
                        href="/upload",
                    ),
                    spacing="3",
                    align="center",
                    padding="4em",
                ),
                rx.text("")
            ),

            # ── CHAT HISTORY ────────────────────────
            rx.vstack(
                rx.foreach(ChatState.history, chat_bubble),
                spacing="4",
                width="100%",
                align="start",
            ),

            # ── LOADING ────────────────────────────
            rx.cond(
                ChatState.is_loading,
                rx.hstack(
                    rx.spinner(),
                    rx.text("Thinking…"),
                ),
                rx.text("")
            ),

            # ── ERROR ─────────────────────────────
            rx.cond(
                ChatState.error_msg != "",
                rx.text(ChatState.error_msg, color="red"),
                rx.text("")
            ),

            # ── INPUT ─────────────────────────────
            rx.hstack(
                rx.input(
                    placeholder="Ask a question...",
                    value=ChatState.question,
                    on_change=ChatState.set_question,
                    flex="1",
                ),
                rx.button(
                    "Send",
                    on_click=ChatState.ask,   # ✅ correct function
                ),
                width="100%",
            ),

            spacing="4",
            padding="2em",
            width="100%",
            max_width="800px",
            margin="0 auto",
        ),

        footer(),
    )
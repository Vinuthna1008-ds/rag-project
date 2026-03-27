"""pages/history.py"""

import reflex as rx
from components.navbar import navbar
from components.footer import footer
from states.rag_state import ChatState


# ── CARD ──────────────────────────────────────────
def history_card(item) -> rx.Component:
    return rx.box(

        rx.vstack(

            # Question
            rx.hstack(
                rx.badge("Q", color_scheme="violet"),
                rx.text(item.question, font_weight="600", size="3"),
            ),

            # Answer
            rx.hstack(
                rx.badge("A", color_scheme="green"),
                rx.text(item.answer, size="3", color="gray"),
            ),

            # ✅ FIXED: sources is STRING now
            rx.cond(
                item.sources != "",
                rx.hstack(
                    rx.text("Sources:", size="1", color="gray"),
                    rx.text(item.sources, size="1"),
                ),
                rx.text("")
            ),

            align="start",
            spacing="2",
        ),

        padding="1.2em",
        border="1px solid #e5e7eb",
        border_radius="12px",
        background="white",
        width="100%",
        box_shadow="0 1px 4px rgba(0,0,0,0.05)",
    )


# ── PAGE ─────────────────────────────────────────
@rx.page(route="/history")
def history() -> rx.Component:
    return rx.vstack(

        navbar(),

        rx.vstack(

            # Header
            rx.hstack(
                rx.heading("📜 Chat History", size="6"),
                rx.spacer(),

                rx.button(
                    "🗑 Clear",
                    on_click=ChatState.clear_history,
                    color_scheme="red",
                    variant="soft",
                    size="2",
                ),

                rx.button(
                    "⬇ Download",
                    on_click=ChatState.download_chat,
                    color_scheme="green",
                    size="2",
                ),
            ),

            # Empty state
            rx.cond(
                ChatState.history.length() == 0,

                rx.vstack(
                    rx.text("📭", size="8"),
                    rx.text("No conversation history yet.", color="gray"),
                    align="center",
                    padding="4em",
                ),

                # History list
                rx.vstack(
                    rx.foreach(ChatState.history, history_card),
                    spacing="4",
                    width="100%",
                ),
            ),

            spacing="5",
            padding="2em",
            width="100%",
            max_width="800px",
            margin="0 auto",
        ),

        footer(),

        spacing="0",
        background="#f8f9ff",
        min_height="100vh",
    )
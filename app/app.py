import reflex as rx
from app.components.navbar import navbar
from app.video import video_page


def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Create Whiteboard Explainer Videos with Prompts / Documents",
                    class_name="text-5xl md:text-7xl font-bold text-center text-white leading-tight tracking-tighter",
                ),
                rx.el.p(
                    "Experience the best video AI model for professional explainer videos.",
                    class_name="text-lg md:text-xl text-gray-400 mt-6 text-center max-w-2xl",
                ),
                rx.el.a(
                    rx.el.button(
                        "Golpo Video",
                        rx.icon("arrow-right", class_name="ml-2"),
                        class_name="bg-white text-black font-semibold px-8 py-4 rounded-full mt-10 text-lg hover:bg-gray-200 transition-transform hover:scale-105 flex items-center shadow-lg",
                    ),
                    href="/video",
                ),
                class_name="flex flex-col items-center justify-center p-8",
            ),
            class_name="container mx-auto flex items-center justify-center min-h-[calc(100vh-80px)]",
        ),
        class_name="font-['Roboto'] bg-black",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(video_page, route="/video")
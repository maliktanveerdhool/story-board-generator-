import reflex as rx


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.h1("Golpo", class_name="text-2xl font-bold text-white"),
                    href="/",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        "Book a Demo",
                        class_name="text-white font-medium px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors",
                    ),
                    href="#",
                ),
                rx.el.a(
                    rx.el.button(
                        "Golpo Video",
                        class_name="bg-white text-black font-medium px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors",
                    ),
                    href="/video",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        class_name="w-full bg-black/50 backdrop-blur-md sticky top-0 z-50 border-b border-gray-800",
    )
import reflex as rx
from app.components.navbar import navbar
from app.states.video_state import VideoState, UPLOAD_ID


def _progress_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                VideoState.progress < 100,
                f"bg-blue-500 h-2.5 rounded-full transition-all duration-300",
                f"bg-green-500 h-2.5 rounded-full transition-all duration-300",
            ),
            style={"width": VideoState.progress.to_string() + "%"},
        ),
        class_name="w-full bg-gray-700 rounded-full h-2.5 mt-4",
    )


def video_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Video Settings", class_name="text-xl font-semibold text-white mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Duration", class_name="text-gray-400 text-sm font-medium mb-2"
                ),
                rx.el.select(
                    rx.el.option("15s", value="15"),
                    rx.el.option("30s", value="30"),
                    rx.el.option("60s", value="60"),
                    rx.el.option("90s", value="90"),
                    value=VideoState.duration,
                    on_change=VideoState.set_duration,
                    class_name="w-full p-2 bg-gray-800 border border-gray-700 rounded-md text-white",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Style", class_name="text-gray-400 text-sm font-medium mb-2"
                ),
                rx.el.select(
                    rx.el.option("Whiteboard", value="Whiteboard"),
                    rx.el.option("Animated", value="Animated"),
                    rx.el.option("Sketch", value="Sketch"),
                    value=VideoState.style,
                    on_change=VideoState.set_style,
                    class_name="w-full p-2 bg-gray-800 border border-gray-700 rounded-md text-white",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Voice", class_name="text-gray-400 text-sm font-medium mb-2"
                ),
                rx.el.select(
                    rx.el.option("Male", value="Male"),
                    rx.el.option("Female", value="Female"),
                    rx.el.option("Neutral", value="Neutral"),
                    value=VideoState.voice_type,
                    on_change=VideoState.set_voice_type,
                    class_name="w-full p-2 bg-gray-800 border border-gray-700 rounded-md text-white",
                ),
                class_name="flex-1",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4",
        ),
        class_name="w-full max-w-2xl mt-8",
    )


def video_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Create your video",
                    class_name="text-4xl md:text-5xl font-bold text-white mb-4",
                ),
                rx.el.p(
                    "Enter a prompt or upload a document to get started.",
                    class_name="text-lg text-gray-400 mb-8",
                ),
                rx.el.div(
                    rx.el.textarea(
                        default_value=VideoState.prompt,
                        on_change=VideoState.set_prompt,
                        placeholder="Enter a detailed prompt for your video...",
                        class_name="w-full p-4 bg-gray-900 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-h-[150px]",
                    ),
                    rx.upload.root(
                        rx.el.div(
                            rx.icon(
                                tag="cloud_upload", class_name="w-8 h-8 text-gray-400"
                            ),
                            rx.el.p(
                                "Drag & drop files here, or click to select files",
                                class_name="text-gray-400",
                            ),
                            class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-700 rounded-lg bg-gray-900 hover:bg-gray-800 transition-colors w-full cursor-pointer mt-4",
                        ),
                        id=UPLOAD_ID,
                        accept={"application/pdf": [".pdf"], "text/plain": [".txt"]},
                        multiple=True,
                        class_name="w-full",
                    ),
                    rx.el.div(
                        rx.foreach(
                            rx.selected_files(UPLOAD_ID),
                            lambda file: rx.el.div(
                                rx.icon("file-text", class_name="mr-2"),
                                file,
                                class_name="flex items-center text-sm p-2 bg-gray-800 rounded-md text-white",
                            ),
                        ),
                        class_name="mt-4 space-y-2",
                    ),
                    video_settings(),
                    rx.el.button(
                        rx.cond(
                            VideoState.is_generating,
                            rx.el.div(
                                rx.spinner(class_name="mr-2"),
                                "Generating...",
                                class_name="flex items-center",
                            ),
                            "Generate Video",
                        ),
                        on_click=VideoState.trigger_generation,
                        disabled=VideoState.is_generating,
                        class_name="w-full bg-white text-black font-semibold px-8 py-4 rounded-full mt-8 text-lg hover:bg-gray-200 transition-transform hover:scale-105 flex items-center justify-center shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed",
                    ),
                    rx.cond(VideoState.is_generating, _progress_bar(), None),
                    rx.cond(
                        VideoState.generation_status == "complete",
                        video_preview(),
                        None,
                    ),
                    class_name="flex flex-col w-full max-w-2xl",
                ),
                video_gallery(),
                class_name="flex flex-col items-center justify-center text-center p-8",
            ),
            class_name="container mx-auto flex items-center justify-center min-h-[calc(100vh-80px)] flex-col",
        ),
        class_name="font-['Roboto'] bg-black",
    )


def video_preview() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Generated Video", class_name="text-2xl font-semibold text-white my-6"
        ),
        rx.video(
            url=VideoState.generated_video_url,
            width="100%",
            height="auto",
            playing=True,
            controls=True,
            class_name="rounded-lg border border-gray-700 bg-gray-900",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("download", class_name="mr-2"),
                "Download",
                on_click=rx.download(
                    url=VideoState.generated_video_url, filename="golpo_video.mp4"
                ),
                class_name="bg-gray-700 text-white font-medium px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors flex items-center",
            ),
            rx.el.button(
                rx.icon("share-2", class_name="mr-2"),
                "Share",
                on_click=[
                    rx.set_clipboard(VideoState.generated_video_url),
                    rx.toast.info("Video link copied to clipboard!"),
                ],
                class_name="bg-gray-700 text-white font-medium px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors flex items-center",
            ),
            class_name="flex items-center justify-center gap-4 mt-4",
        ),
        class_name="w-full max-w-2xl mt-8 p-4 bg-gray-900/50 rounded-lg",
    )


def video_gallery() -> rx.Component:
    return rx.el.div(
        rx.cond(
            VideoState.video_history.length() > 0,
            rx.el.div(
                rx.el.h3(
                    "Video History", class_name="text-2xl font-semibold text-white mb-6"
                ),
                rx.el.div(
                    rx.foreach(
                        VideoState.video_history,
                        lambda video, index: rx.el.div(
                            rx.video(
                                url=video["url"],
                                width="100%",
                                height="auto",
                                class_name="rounded-t-lg cursor-pointer",
                                on_click=VideoState.select_video_from_history(video),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    video["prompt"],
                                    class_name="text-sm text-gray-300 truncate",
                                ),
                                rx.el.p(
                                    f"{video['style']} - {video['duration']}s - {video['voice']}",
                                    class_name="text-xs text-gray-500 mt-1",
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon(tag="download", class_name="w-4 h-4"),
                                        on_click=rx.download(
                                            url=video["url"], filename="golpo_video.mp4"
                                        ),
                                        class_name="p-2 bg-gray-700 rounded-md hover:bg-gray-600",
                                    ),
                                    rx.el.button(
                                        rx.icon(tag="share-2", class_name="w-4 h-4"),
                                        on_click=[
                                            rx.set_clipboard(video["url"]),
                                            rx.toast.info("Link copied!"),
                                        ],
                                        class_name="p-2 bg-gray-700 rounded-md hover:bg-gray-600",
                                    ),
                                    rx.el.button(
                                        rx.icon(tag="refresh-cw", class_name="w-4 h-4"),
                                        on_click=VideoState.regenerate_video(video),
                                        class_name="p-2 bg-gray-700 rounded-md hover:bg-gray-600",
                                    ),
                                    class_name="flex items-center gap-2 mt-2",
                                ),
                                class_name="p-3",
                            ),
                            class_name="bg-gray-800 rounded-lg border border-gray-700 hover:border-blue-500 transition-all",
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4",
                ),
                class_name="w-full max-w-6xl mt-12",
            ),
        ),
        class_name="w-full flex justify-center px-4",
    )
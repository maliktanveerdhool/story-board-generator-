import reflex as rx
import asyncio

UPLOAD_ID = "upload_area"


class VideoState(rx.State):
    """State for the video creation page."""

    prompt: str = ""
    uploaded_files: list[str] = []
    is_generating: bool = False
    duration: str = "30"
    style: str = "Whiteboard"
    voiceover_enabled: bool = True
    voice_type: str = "Male"
    generation_status: str = "idle"
    progress: int = 0
    generated_video_url: str = ""
    video_history: list[dict[str, str]] = []

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file uploads."""
        if not files:
            return
        for file in files:
            upload_data = await file.read()
            output_path = rx.get_upload_dir() / file.name
            with output_path.open("wb") as f:
                f.write(upload_data)
            self.uploaded_files.append(file.name)

    @rx.event
    def trigger_generation(self):
        """Event to trigger upload and video generation."""
        return [
            VideoState.handle_upload(rx.upload_files(upload_id=UPLOAD_ID)),
            VideoState.generate_video,
        ]

    @rx.event
    async def generate_video(self):
        """Generate video from prompt and/or files."""
        if not self.prompt and (not self.uploaded_files):
            yield rx.toast.error("Please enter a prompt or upload a file.")
            return
        self.is_generating = True
        self.generation_status = "generating"
        self.progress = 0
        yield rx.toast.info("Video generation started!")
        for i in range(101):
            self.progress = i
            await asyncio.sleep(0.05)
            yield
        self.generated_video_url = "/placeholder_video.mp4"
        video_data = {
            "url": self.generated_video_url,
            "prompt": self.prompt,
            "duration": self.duration,
            "style": self.style,
            "voice": self.voice_type,
        }
        self.video_history.insert(0, video_data)
        self.generation_status = "complete"
        yield rx.toast.success("Video generated successfully!")
        self.is_generating = False

    @rx.event
    def select_video_from_history(self, video: dict):
        """Select a video from the history to preview."""
        self.generated_video_url = video["url"]
        self.prompt = video["prompt"]
        self.duration = video["duration"]
        self.style = video["style"]
        self.voice_type = video["voice"]

    @rx.event
    def regenerate_video(self, video_data: dict):
        """Set generation parameters based on a historical video for regeneration."""
        self.prompt = video_data["prompt"]
        self.duration = video_data["duration"]
        self.style = video_data["style"]
        self.voice_type = video_data["voice"]
        yield rx.toast.info("Settings restored. Click 'Generate Video' to regenerate.")
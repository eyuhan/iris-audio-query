import base64
import json

from iop import BusinessOperation
from sqlmodel import Session

from app.config import TwelveLabsConfig
from app.database import engine, db
from twelvelabs_client.twelvelabs_client import create_client, embed_audio, File
from models.audio import AudioSegment
from interop.msg import HttpMessageRequest, HttpMessageResponse


class EmbedBO(BusinessOperation):
    twelvelabs_client = None

    def on_init(self):
        self.log_to_console = True
        if not TwelveLabsConfig.is_configured():
            self.log_warning("TwelveLabs credentials not configured")
            self.twelvelabs_client = None
        else:
            self.twelvelabs_client = create_client(api_key=TwelveLabsConfig.API_KEY)

    def on_message(
        self, message_request: HttpMessageRequest
    ) -> HttpMessageResponse:
        try:
            if not self.twelvelabs_client:
                self.log_error("TwelveLabs client not available")
                return HttpMessageResponse(
                    status=503,
                    headers={"Content-Type": "application/json"},
                    body=json.dumps({"error": "Twilio service not configured"})
                )

            filename, encoded_file, media_type = message_request.file
            file = base64.b64decode(encoded_file)

            object_id = self.store_audio(
                filename=filename,
                file=file,
                media_type=media_type
            )
            self.embed_audio(
                object_id=object_id,
                file=file
            )

            return HttpMessageResponse(
                status=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps({"success": True})
            )

        except Exception as e:
            self.log_error(f"Error processing batch request: {str(e)}")
            return HttpMessageResponse(
                status=500,
                headers={"Content-Type": "application/json"},
                body=json.dumps({"error": str(e)})
            )


    def store_audio(self, filename: str, file: File, media_type: str):
        self.log_info("Storing audio file...")

        stream_object = db.classMethodObject("%Stream.GlobalBinary", "%New")
        stream_object.invoke("Write", file)
        stream_object.invokeVoid("%Save")

        audio_object = db.classMethodObject("IrisAudioQuery.Audio", "%New")
        audio_object.set("FileName", filename)
        audio_object.set("AudioData", stream_object)
        audio_object.set("MediaType", media_type)
        audio_object.invokeVoid("%Save")

        object_id = audio_object.invoke("%Id")

        self.log_info("Successfully stored audio file.")

        return object_id


    def embed_audio(self, object_id: str, file: File):
        self.log_info("Embedding audio...")
        embeddings = embed_audio(self.twelvelabs_client, file)
        self.log_info("Successfully embedded audio.")

        self.log_info("Storing audio embeddings...")
        segments = [AudioSegment(object_id=object_id, embedding=embedding) for embedding in embeddings]
        with Session(engine) as session:
            session.add_all(segments)
            session.commit()
        self.log_info("Successfully stored audio embeddings.")



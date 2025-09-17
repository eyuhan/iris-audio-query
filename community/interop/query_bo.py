import base64
import json
from typing import List, Any

from iop import BusinessOperation
from sqlmodel import Session, text, select
from baml_py import Audio

from app.config import TwelveLabsConfig
from app.database import engine, db
from baml_client.sync_client import b
from twelvelabs_client.twelvelabs_client import create_client, embed_text, File
from models.audio import AudioSegment
from interop.msg import HttpMessageRequest, HttpMessageResponse


NUM_SEARCH_EMBEDDINGS = 5


class QueryBO(BusinessOperation):
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

            object_ids = self.search_query(
                query=message_request.query
            )
            audio_files = self.fetch_audio(
                object_ids=object_ids
            )
            res = self.infer_embeddings(
                query=message_request.query,
                audio_files=audio_files
            )

            return HttpMessageResponse(
                status=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps(res)
            )

        except Exception as e:
            self.log_error(f"Error processing batch request: {str(e)}")
            return HttpMessageResponse(
                status=500,
                headers={"Content-Type": "application/json"},
                body=json.dumps({"error": str(e)})
            )


    def search_query(self, query: str) -> Any:
        self.log_info("Embedding query...")
        query_segments = embed_text(self.twelvelabs_client, query)
        self.log_info("Successfully embedded query.")

        self.log_info("Searching query...")
        search_query = text(
                    "SELECT TOP :num_embeddings object_id, embedding FROM audio_segments "
                    "ORDER BY VECTOR_COSINE(embedding, TO_VECTOR(:query_embedding, FLOAT)) DESC"
                )
        with Session(engine) as session:
            result = session.execute(
                search_query,
                {
                    "num_embeddings": NUM_SEARCH_EMBEDDINGS,
                    "query_embedding": ",".join(str(f) for f in query_segments)
                }
            )
            rows = result.fetchall()
            object_ids: List[int] = [row[0] for row in rows]
        self.log_info("Successfully searched query.")

        return object_ids


    def fetch_audio(self, object_ids: List[int]):
        self.log_info("Fetching audio...")

        audio_files: List[File] = []
        for object_id in object_ids:
            audio_object = db.classMethodObject("IrisAudioQuery.Audio", "%OpenId", object_id)
            filename = audio_object.get("FileName")
            media_type = audio_object.get("MediaType")

            stream_object = audio_object.get("AudioData")
            audio_raw = stream_object.invoke("Read").encode("utf-8")
            audio_base64 = base64.b64encode(audio_raw).decode("utf-8")
            audio_files.append((filename, audio_base64, media_type))

        self.log_info("Successfully fetched audio...")

        return audio_files


    def infer_embeddings(self, query: str, audio_files: List[File]) -> Any:
        self.log_info("Inferring query...")
        audio_objects = [Audio.from_base64(media_type=media_type, base64=file) for filename, file, media_type in audio_files]
        answer = b.QueryAudio(query=query, audio_files=audio_objects)
        self.log_info("Successfully inferred query.")

        return answer
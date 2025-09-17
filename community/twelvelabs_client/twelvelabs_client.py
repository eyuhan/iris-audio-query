from twelvelabs import TwelveLabs
from twelvelabs.core import File


EMBEDDING_MODEL_NAME = "Marengo-retrieval-2.7"


def create_client(api_key):
    return TwelveLabs(api_key=api_key)


def embed_audio(client: TwelveLabs, audio: File):
    res = client.embed.create(
        model_name=EMBEDDING_MODEL_NAME,
        audio_file=audio
    )

    if not hasattr(res, 'audio_embedding') or not res.audio_embedding.segments:
        raise RuntimeError

    return res.audio_embedding.segments


def embed_text(client: TwelveLabs, text: str):
    res = client.embed.create(
        model_name=EMBEDDING_MODEL_NAME,
        text=text
    )

    if not hasattr(res, 'text_embedding') or not res.text_embedding.segments:
        raise RuntimeError

    return res.text_embedding.segments
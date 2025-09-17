import base64

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query, Form

from iop import Director

from models.schemas import AudioUploadRequest, AudioUploadResponse, AudioQueryRequest, AudioQueryResponse

router = APIRouter(prefix="/audio", tags=["posts"])

try:
    bs = Director.create_python_business_service('BS')
except Exception as e:
    bs = None
    print(f"Warning: Could not initialize IRIS business service: {e}")

@router.post("/upload", response_model=AudioUploadResponse, status_code=status.HTTP_200_OK)
async def upload_audio(file: UploadFile = File(...)):
    if bs is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IRIS business service not available"
        )

    try:
        filename = file.filename
        media_type = file.content_type

        raw_file = await file.read()
        encoded_file = base64.b64encode(raw_file).decode('ascii')

        response = bs.on_message(AudioUploadRequest(file=(filename, encoded_file, media_type)))
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
            )
        return {"success": True}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audio upload failed: {str(e)}"
        )

@router.get("/query", status_code=status.HTTP_200_OK)
async def query_audio(query: str = Query(...)):
    if bs is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IRIS business service not available"
        )

    try:
        response = bs.on_message(AudioQueryRequest(query=query))
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
            )
        return response.body

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audio query failed: {str(e)}"
        )

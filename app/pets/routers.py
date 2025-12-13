from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from typing import List
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil
from app.pets.schemas import SPetCreate, SPetResponse, SPetUpdate
from app.pets.services import PetService
from app.users.dependencies import get_current_user
from app.users.models import User
from app.utils.files import ensure_media_dir, secure_filename, validate_image_and_save, MEDIA_ROOT

from app.ml.embeddings import image_to_embedding
from app.ml.breed_classifier import dog_breed_model

router = APIRouter(prefix="/pets", tags=["Питомцы"])


@router.get("/", response_model=List[SPetResponse])
async def get_pets():
    return await PetService.find_all()


@router.get("/{pet_id}", response_model=SPetResponse)
async def get_pet(pet_id: int):
    pet = await PetService.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return pet


@router.post("/", response_model=SPetResponse, status_code=201)
async def create_pet(pet: SPetCreate, current_user: User = Depends(get_current_user)):
    payload = pet.model_dump()
    payload["owner_id"] = current_user.id
    new_pet = await PetService.create_pet(payload)
    return new_pet


@router.put("/{pet_id}", response_model=SPetResponse)
async def update_pet(pet_id: int, pet_update: SPetUpdate, current_user: User = Depends(get_current_user)):
    pet_obj = await PetService.find_by_id(pet_id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Питомец не найден")

    if pet_obj.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на изменение этого питомца")

    update_data = pet_update.model_dump(exclude_unset=True)
    updated = await PetService.update_pet(pet_id, update_data)
    return updated


@router.delete("/{pet_id}", status_code=status.HTTP_200_OK)
async def delete_pet(pet_id: int, current_user: User = Depends(get_current_user)):
    pet_obj = await PetService.find_by_id(pet_id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Питомец не найден")

    if pet_obj.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на удаление этого питомца")

    ok = await PetService.delete_pet(pet_id)
    if not ok:
        raise HTTPException(status_code=500, detail="Ошибка при удалении")
    return {"detail": "Питомец удалён"}

@router.post("/{pet_id}/upload_photo", response_model=SPetResponse)
async def upload_pet_photo(pet_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    pet = await PetService.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на загрузку фото для этого питомца")

    ensure_media_dir()

    fname = secure_filename(file.filename)
    dest = Path("media/pets") / str(pet_id)
    dest.mkdir(parents=True, exist_ok=True)
    file_path = dest / fname

    try:
        validate_image_and_save(file, file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        file.file.close()

    photo_url = f"/media/pets/{pet_id}/{fname}"
    try:
        emb = image_to_embedding(str(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {e}")

    updated = await PetService.update_pet(pet_id, {"photo_url": photo_url, "embedding": emb})
    return updated


@router.post("/find_similar")
async def find_similar_pets(type: str, file: UploadFile = File(...)):
    """
    Загружает фото -> считает embedding -> ищет 5 самых похожих питомцев этого типа
    """
    temp_path = Path("media/temp")
    temp_path.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    temp_file = temp_path / f"query{ext}"

    data = file.file.read()
    with open(temp_file, "wb") as f:
        f.write(data)
    file.file.close()

    try:
        query_emb = image_to_embedding(str(temp_file))
    except Exception as e:
        temp_file.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {e}")

    result = await PetService.find_similar_by_embedding(type, query_emb, top_k=5)
    temp_file.unlink(missing_ok=True)
    return result


@router.post("/predict_breed")
async def predict_breed(file: UploadFile = File(...)):
    """
    Принимает фото собаки -> возвращает породу.
    """

    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = dog_breed_model.predict(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки изображения: {e}")

    return result
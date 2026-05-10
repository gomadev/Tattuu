"""Endpoints para gerenciamento de tatuadores favoritos."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Favorite, User, Artist
from app.schemas.schemas import ArtistResponse

router = APIRouter(prefix="/api/v1/favorites", tags=["favorites"])


@router.post("/{artist_id}", status_code=status.HTTP_201_CREATED)
def adicionar_favorito(artist_id: int, user_id: int, db: Session = Depends(get_db)) -> dict:
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    artista = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    
    favorito_existente = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.artist_id == artist_id
    ).first()
    
    if favorito_existente:
        raise HTTPException(status_code=409, detail="Tatuador já está nos favoritos")
    
    novo_favorito = Favorite(user_id=user_id, artist_id=artist_id)
    db.add(novo_favorito)
    db.commit()
    return {"mensagem": "Tatuador adicionado aos favoritos"}


@router.get("/usuario/{user_id}", response_model=list[ArtistResponse])
def listar_favoritos(user_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> list[ArtistResponse]:
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    favoritos = db.query(Artist).join(
        Favorite, Artist.id == Favorite.artist_id
    ).filter(
        Favorite.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return favoritos


@router.delete("/{artist_id}")
def remover_favorito(artist_id: int, user_id: int, db: Session = Depends(get_db)) -> dict:
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    artista = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    
    favorito = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.artist_id == artist_id
    ).first()
    
    if not favorito:
        raise HTTPException(status_code=404, detail="Tatuador não está nos favoritos")
    
    db.delete(favorito)
    db.commit()
    return {"mensagem": "Tatuador removido dos favoritos"}


@router.get("/usuario/{user_id}/verificar/{artist_id}")
def verificar_favorito(user_id: int, artist_id: int, db: Session = Depends(get_db)) -> dict:
    favorito = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.artist_id == artist_id
    ).first()
    
    return {"eh_favorito": favorito is not None}

"""Endpoints para gerenciamento de avaliações e comentários."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Rating, User, Artist
from app.schemas.schemas import RatingResponse, RatingCreate

router = APIRouter(prefix="/api/v1/ratings", tags=["ratings"])


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def criar_avaliacao(avaliacao: RatingCreate, db: Session = Depends(get_db)) -> RatingResponse:
    usuario = db.query(User).filter(User.id == avaliacao.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    artista = db.query(Artist).filter(Artist.id == avaliacao.artist_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    
    avaliacao_existente = db.query(Rating).filter(
        Rating.user_id == avaliacao.user_id,
        Rating.artist_id == avaliacao.artist_id
    ).first()
    
    if avaliacao_existente:
        raise HTTPException(status_code=409, detail="Usuário já avaliou este tatuador")
    
    nova_avaliacao = Rating(**avaliacao.dict())
    db.add(nova_avaliacao)
    db.flush()
    
    resultado = db.query(
        func.avg(Rating.score).label("media"),
        func.count(Rating.id).label("total")
    ).filter(Rating.artist_id == avaliacao.artist_id).first()
    
    artista.rating = float(resultado.media) if resultado.media else 0.0
    artista.total_ratings = resultado.total
    
    db.add(artista)
    db.commit()
    db.refresh(nova_avaliacao)
    return nova_avaliacao


@router.get("/{rating_id}", response_model=RatingResponse)
def obter_avaliacao(rating_id: int, db: Session = Depends(get_db)) -> RatingResponse:
    avaliacao = db.query(Rating).filter(Rating.id == rating_id).first()
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao


@router.get("/artista/{artist_id}", response_model=list[RatingResponse])
def listar_avaliacoes_por_artista(artist_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> list[RatingResponse]:
    artista = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    
    avaliacoes = db.query(Rating).filter(
        Rating.artist_id == artist_id
    ).order_by(Rating.created_at.desc()).offset(skip).limit(limit).all()
    return avaliacoes


@router.get("/usuario/{user_id}", response_model=list[RatingResponse])
def listar_avaliacoes_por_usuario(user_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> list[RatingResponse]:
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    avaliacoes = db.query(Rating).filter(
        Rating.user_id == user_id
    ).order_by(Rating.created_at.desc()).offset(skip).limit(limit).all()
    return avaliacoes


@router.put("/{rating_id}", response_model=RatingResponse)
def atualizar_avaliacao(rating_id: int, avaliacao_update: RatingCreate, db: Session = Depends(get_db)) -> RatingResponse:
    avaliacao = db.query(Rating).filter(Rating.id == rating_id).first()
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    artista_id_anterior = avaliacao.artist_id
    
    avaliacao.score = avaliacao_update.score
    avaliacao.comment = avaliacao_update.comment
    
    db.add(avaliacao)
    db.flush()
    
    resultado = db.query(
        func.avg(Rating.score).label("media"),
        func.count(Rating.id).label("total")
    ).filter(Rating.artist_id == artista_id_anterior).first()
    
    artista = db.query(Artist).filter(Artist.id == artista_id_anterior).first()
    artista.rating = float(resultado.media) if resultado.media else 0.0
    artista.total_ratings = resultado.total
    
    db.add(artista)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_avaliacao(rating_id: int, db: Session = Depends(get_db)) -> None:
    avaliacao = db.query(Rating).filter(Rating.id == rating_id).first()
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    artista_id = avaliacao.artist_id
    db.delete(avaliacao)
    db.flush()
    
    resultado = db.query(
        func.avg(Rating.score).label("media"),
        func.count(Rating.id).label("total")
    ).filter(Rating.artist_id == artista_id).first()
    
    artista = db.query(Artist).filter(Artist.id == artista_id).first()
    artista.rating = float(resultado.media) if resultado.media else 0.0
    artista.total_ratings = resultado.total
    
    db.add(artista)
    db.commit()
    return None

"""Endpoints de busca avançada de tatuadores."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.models import Artist, Style, Rating
from app.schemas.schemas import ArtistDetailResponse

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("/artistas", response_model=list[ArtistDetailResponse])
def buscar_artistas(
    style_id: Optional[int] = Query(None, description="ID do estilo"),
    location: Optional[str] = Query(None, description="Localização (busca parcial)"),
    min_rating: Optional[float] = Query(0, ge=0, le=5, description="Avaliação mínima"),
    max_rating: Optional[float] = Query(5, ge=0, le=5, description="Avaliação máxima"),
    min_experience: Optional[int] = Query(None, ge=0, description="Experiência mínima em anos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
) -> list[ArtistDetailResponse]:
    query = db.query(Artist)
    
    if style_id is not None:
        query = query.join(Artist.styles).filter(Style.id == style_id)
    
    if location:
        query = query.filter(Artist.location.ilike(f"%{location}%"))
    
    if min_rating is not None:
        query = query.filter(Artist.rating >= min_rating)
    
    if max_rating is not None:
        query = query.filter(Artist.rating <= max_rating)
    
    if min_experience is not None:
        query = query.filter(Artist.years_experience >= min_experience)
    
    artistas = query.offset(skip).limit(limit).all()
    return artistas


@router.get("/artistas/recomendados", response_model=list[ArtistDetailResponse])
def obter_recomendados(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
) -> list[ArtistDetailResponse]:
    artistas = db.query(Artist).filter(
        Artist.total_ratings > 0
    ).order_by(Artist.rating.desc()).limit(limit).all()
    
    return artistas


@router.get("/artistas/novos", response_model=list[ArtistDetailResponse])
def obter_artistas_novos(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
) -> list[ArtistDetailResponse]:

    artistas = db.query(Artist).order_by(Artist.created_at.desc()).limit(limit).all()
    return artistas


@router.get("/artistas/experiencia", response_model=list[ArtistDetailResponse])
def buscar_por_experiencia(
    min_years: int = Query(0, ge=0, description="Experiência mínima"),
    max_years: Optional[int] = Query(None, description="Experiência máxima"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
) -> list[ArtistDetailResponse]:
    query = db.query(Artist).filter(Artist.years_experience >= min_years)
    
    if max_years is not None:
        query = query.filter(Artist.years_experience <= max_years)
    
    artistas = query.offset(skip).limit(limit).all()
    return artistas


@router.get("/estilos", response_model=list)
def listar_estilos(db: Session = Depends(get_db)) -> list[dict]:

    estilos = db.query(Style).all()
    return [{"id": e.id, "name": e.name, "description": e.description} for e in estilos]


@router.get("/artistas/estilo/{style_id}/top", response_model=list[ArtistDetailResponse])
def obter_top_artistas_por_estilo(
    style_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
) -> list[ArtistDetailResponse]:
    estilo = db.query(Style).filter(Style.id == style_id).first()
    if not estilo:
        raise HTTPException(status_code=404, detail="Estilo não encontrado")
    
    artistas = db.query(Artist).join(
        Artist.styles
    ).filter(
        Style.id == style_id,
        Artist.total_ratings > 0
    ).order_by(Artist.rating.desc()).limit(limit).all()
    
    return artistas

"""Rotas da API para gerenciamento de tatuadores."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Artist, Style, User
from app.schemas.schemas import ArtistCreate, ArtistResponse, ArtistDetailResponse, ArtistUpdate

router = APIRouter(prefix="/artists", tags=["artists"])


@router.post("/", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)) -> ArtistResponse:
    user = db.query(User).filter(User.id == artist.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    db_artist = Artist(
        user_id=artist.user_id,
        bio=artist.bio,
        location=artist.location,
        latitude=artist.latitude,
        longitude=artist.longitude,
        years_experience=artist.years_experience
    )
    
    if artist.style_ids:
        styles = db.query(Style).filter(Style.id.in_(artist.style_ids)).all()
        db_artist.styles = styles
    
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    
    return db_artist


@router.get("/", response_model=list[ArtistResponse])
def list_artists(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    style_id: int = Query(None),
    location: str = Query(None),
    db: Session = Depends(get_db)
) -> list[ArtistResponse]:
    query = db.query(Artist)
    
    if style_id:
        query = query.filter(Artist.styles.any(Style.id == style_id))
    
    if location:
        query = query.filter(Artist.location.ilike(f"%{location}%"))
    
    return query.offset(skip).limit(limit).all()


@router.get("/{artist_id}", response_model=ArtistDetailResponse)
def get_artist(artist_id: int, db: Session = Depends(get_db)) -> ArtistDetailResponse:
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tatuador não encontrado"
        )
    
    return artist


@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    artist_update: ArtistUpdate,
    db: Session = Depends(get_db)
) -> ArtistResponse:
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tatuador não encontrado"
        )
    
    update_data = artist_update.model_dump(exclude_unset=True)
    style_ids = update_data.pop('style_ids', None)
    
    for field, value in update_data.items():
        setattr(artist, field, value)
    
    if style_ids is not None:
        styles = db.query(Style).filter(Style.id.in_(style_ids)).all()
        artist.styles = styles
    
    db.commit()
    db.refresh(artist)
    
    return artist

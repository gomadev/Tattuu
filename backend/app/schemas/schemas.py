"""Esquemas Pydantic para validação de requisições e respostas."""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str = Field(..., description="Email ou username")
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class StyleBase(BaseModel):
    name: str
    description: Optional[str] = None


class StyleResponse(StyleBase):
    id: int
    
    class Config:
        from_attributes = True


class ArtistBase(BaseModel):
    bio: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    years_experience: Optional[int] = None


class ArtistCreate(ArtistBase):
    user_id: int
    style_ids: Optional[list[int]] = []


class ArtistUpdate(ArtistBase):
    style_ids: Optional[list[int]] = None


class ArtistResponse(ArtistBase):
    id: int
    user_id: int
    rating: float
    total_ratings: int
    created_at: datetime
    styles: list[StyleResponse] = []
    
    class Config:
        from_attributes = True


class ArtistDetailResponse(ArtistResponse):
    portfolios: list['PortfolioResponse'] = []
    ratings: list['RatingResponse'] = []


class PortfolioBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    style_id: Optional[int] = None


class PortfolioCreate(PortfolioBase):
    artist_id: int


class PortfolioResponse(PortfolioBase):
    id: int
    artist_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RatingBase(BaseModel):
    score: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    user_id: int
    artist_id: int


class RatingResponse(RatingBase):
    id: int
    user_id: int
    artist_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class EventBase(BaseModel):

    event_type: str
    user_id: Optional[int] = None
    artist_id: Optional[int] = None
    metadata: dict = Field(default_factory=dict)


class EventCreate(EventBase):
    timestamp: datetime = Field(default_factory=datetime.utcnow)


ArtistDetailResponse.model_rebuild()

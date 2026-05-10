"""Modelos ORM com SQLAlchemy."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


artist_styles = Table(
    'artist_styles',
    Base.metadata,
    Column('artist_id', Integer, ForeignKey('artists.id'), primary_key=True),
    Column('style_id', Integer, ForeignKey('styles.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    favorites = relationship("Artist", secondary="favorites", back_populates="favorited_by")


class Artist(Base):
    __tablename__ = "artists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    years_experience = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User")
    portfolios = relationship("Portfolio", back_populates="artist")
    styles = relationship("Style", secondary=artist_styles, back_populates="artists")
    ratings = relationship("Rating", back_populates="artist")


class Style(Base):
    __tablename__ = "styles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    artists = relationship("Artist", secondary=artist_styles, back_populates="styles")


class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=False)
    style_id = Column(Integer, ForeignKey('styles.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    artist = relationship("Artist", back_populates="portfolios")
    style = relationship("Style")


class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    score = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
    artist = relationship("Artist", back_populates="ratings")


class Favorite(Base):
    __tablename__ = "favorites"
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

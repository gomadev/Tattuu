"""Endpoints para gerenciamento de portfólio de tatuadores."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Portfolio, Artist, Style
from app.schemas.schemas import PortfolioResponse, PortfolioCreate

router = APIRouter(prefix="/api/v1/portfolios", tags=["portfolios"])


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def criar_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)) -> PortfolioResponse:
    artista = db.query(Artist).filter(Artist.id == portfolio.artist_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    
    if portfolio.style_id:
        estilo = db.query(Style).filter(Style.id == portfolio.style_id).first()
        if not estilo:
            raise HTTPException(status_code=404, detail="Estilo não encontrado")
    
    novo_portfolio = Portfolio(**portfolio.dict())
    db.add(novo_portfolio)
    db.commit()
    db.refresh(novo_portfolio)
    return novo_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def obter_portfolio(portfolio_id: int, db: Session = Depends(get_db)) -> PortfolioResponse:
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Item de portfólio não encontrado")
    return portfolio


@router.get("/artista/{artist_id}", response_model=list[PortfolioResponse])
def listar_portfolio_por_artista(artist_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)) -> list[PortfolioResponse]:
    artista = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    
    portfolios = db.query(Portfolio).filter(
        Portfolio.artist_id == artist_id
    ).offset(skip).limit(limit).all()
    return portfolios


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def atualizar_portfolio(portfolio_id: int, portfolio_update: PortfolioCreate, db: Session = Depends(get_db)) -> PortfolioResponse:
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Item de portfólio não encontrado")
    
    dados_atualizacao = portfolio_update.dict(exclude_unset=True)
    
    if "style_id" in dados_atualizacao and dados_atualizacao["style_id"]:
        estilo = db.query(Style).filter(Style.id == dados_atualizacao["style_id"]).first()
        if not estilo:
            raise HTTPException(status_code=404, detail="Estilo não encontrado")
    
    for campo, valor in dados_atualizacao.items():
        setattr(portfolio, campo, valor)
    
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_portfolio(portfolio_id: int, db: Session = Depends(get_db)) -> None:
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Item de portfólio não encontrado")
    
    db.delete(portfolio)
    db.commit()
    return None

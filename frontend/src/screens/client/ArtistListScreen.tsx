import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { artistsMock } from '../../data/artists';
import './ArtistListScreen.css';

function getInitials(name: string) {
  return name
    .split(' ')
    .map((w) => w[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

function ArtistCard({ artist }: { artist: (typeof artistsMock)[0] }) {
  const ini = getInitials(artist.name);

  function handleMouseMove(e: React.MouseEvent<HTMLDivElement>) {
    const el = e.currentTarget;
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    el.style.transform = `translateY(-5px) rotateY(${x * 10}deg) rotateX(${-y * 8}deg) scale(1.02)`;
  }

  function handleMouseLeave(e: React.MouseEvent<HTMLDivElement>) {
    e.currentTarget.style.transform = '';
  }

  return (
    <div
      className="artist-card"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      <div className="card-top-glow" />

      <div className="card-img">
        <div className="card-img-inner">
          <div className="img-ring2" />
          <div className="img-ring" />
          <div className="img-initials">{ini}</div>
        </div>
      </div>

      <div className="card-body">
        <div className="card-identity">
          <div className="avatar">{ini}</div>
          <div>
            <div className="card-name">{artist.name}</div>
            <div className="card-handle">{artist.handle ?? `@${artist.name.toLowerCase().replace(' ', '.')}`}</div>
          </div>
        </div>

        <div className="card-bio">{artist.bio}</div>

        <div className="card-tags">
          {artist.styles.map((s) => (
            <span key={s} className="tag">
              {s}
            </span>
          ))}
        </div>

        <button type="button" className="card-cta">
          Ver perfil completo →
        </button>
      </div>
    </div>
  );
}

export function ArtistListScreen() {
  const [tagQuery, setTagQuery] = useState('');
  const navigate = useNavigate();

  const artists = useMemo(() => {
    const query = tagQuery.trim().toLowerCase();

    if (!query) {
      return artistsMock;
    }

    return artistsMock.filter((artist) => {
      return artist.styles.some((style) => style.toLowerCase().includes(query));
    });
  }, [tagQuery]);

  return (
    <>
      <div className="pg">
        <div className="orb orb1" />
        <div className="orb orb2" />
        <div className="orb orb3" />

        <nav className="navbar">
          <div className="logo">
            <em>T</em>attoo
          </div>
          <div className="nav-pill">Descobrir artistas</div>
        </nav>

        <div className="layout">
          <aside className="sidebar">
            <div>
              <div className="s-label">Tags</div>
              <div className="tag-search">
                <input
                  type="text"
                  value={tagQuery}
                  onChange={(event) => setTagQuery(event.target.value)}
                  placeholder="Buscar tag, ex: blackwork"
                  aria-label="Buscar tags"
                />
                {tagQuery && (
                  <button type="button" onClick={() => setTagQuery('')}>
                    Limpar
                  </button>
                )}
              </div>
              <p className="tag-search-hint">
                Filtre os artistas pelas tags dos estilos.
              </p>
              <div className="chips chips--muted">
                {artistsMock
                  .flatMap((artist) => artist.styles)
                  .filter((style, index, all) => all.indexOf(style) === index)
                  .filter((style) => style.toLowerCase().includes(tagQuery.toLowerCase().trim()))
                  .map((style) => (
                    <span key={style} className="chip chip--static">
                      {style}
                    </span>
                  ))}
              </div>
            </div>

            <div>
              <div className="s-label">Navegação</div>
              <div className="nav-links">
                <button
                  type="button"
                  className="nlink"
                  onClick={() => navigate('/client/filtered')}
                >
                  Ver filtrados
                </button>
                <button
                  type="button"
                  className="nlink"
                  onClick={() => navigate('/client/empty')}
                >
                  Simular vazio
                </button>
              </div>
            </div>
          </aside>

          <main className="main">
            <div className="topbar">
              <div className="cnt">
                <b>
                  {artists.length} artista{artists.length !== 1 ? 's' : ''}
                </b>{' '}
                encontrado{artists.length !== 1 ? 's' : ''}
                {tagQuery && ` com tag "${tagQuery}"`}
              </div>

              {tagQuery && (
                <span className="ftag">
                  {tagQuery}
                  <button type="button" onClick={() => setTagQuery('')}>
                    ×
                  </button>
                </span>
              )}
            </div>

            <div className="grid">
              {artists.length > 0 ? (
                artists.map((artist) => (
                  <ArtistCard key={artist.id} artist={artist} />
                ))
              ) : (
                <div className="no-results">
                  <p>Nenhum artista encontrado</p>
                  <button
                    type="button"
                    onClick={() => setTagQuery('')}
                  >
                    Limpar filtros
                  </button>
                </div>
              )}
            </div>
          </main>
        </div>
      </div>
    </>
  );
}

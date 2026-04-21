import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { ArtistCard } from '../../components/ArtistCard';
import { Chip } from '../../components/Chip';
import { SearchBar } from '../../components/SearchBar';
import { artistsMock } from '../../data/artists';

const highlights = ['Blackwork', 'Realismo', 'Fineline', 'Aquarela'];

export function ArtistListScreen() {
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const artists = useMemo(() => {
    const query = search.toLowerCase().trim();
    if (!query) {
      return artistsMock;
    }

    return artistsMock.filter((artist) => {
      return (
        artist.name.toLowerCase().includes(query) ||
        artist.shortDescription.toLowerCase().includes(query) ||
        artist.styles.some((style) => style.toLowerCase().includes(query))
      );
    });
  }, [search]);

  return (
    <main className="screen screen--light">
      <div className="page-frame">
        <div className="client-layout">
          <aside className="client-sidebar">
            <div className="client-sidebar-card">
              <img src="/tattoo_logo_light.png" alt="Tattoo" className="logo-top" />
              <h2>Encontrar tatuadores por estilo</h2>
              <p>
                Uma vitrine web com busca, filtros e cards em grade para destacar profissionais.
              </p>
            </div>

            <div className="client-sidebar-card">
              <h2>Atalhos</h2>
              <div className="client-sidebar-actions">
                <button type="button" className="secondary-button" onClick={() => navigate('/client/filtered')}>
                  Ver versão filtrada
                </button>
                <button type="button" className="secondary-button" onClick={() => navigate('/client/empty')}>
                  Simular sem resultados
                </button>
              </div>
            </div>

            <div className="client-sidebar-card">
              <h2>Estilos em destaque</h2>
              <div className="chip-row">
                {highlights.map((style) => (
                  <Chip key={style} label={style} />
                ))}
              </div>
            </div>
          </aside>

          <section className="client-main">
            <div className="client-toolbar">
              <div className="client-toolbar-head">
                <div className="client-toolbar-title">
                  <strong>Artistas disponíveis</strong>
                  <span>{artists.length} resultado(s) encontrado(s)</span>
                </div>
              </div>
              <SearchBar value={search} placeholder="Busque por nome ou estilo" onChange={setSearch} />
            </div>

            <section className="list-content">
              {artists.map((artist) => (
                <ArtistCard key={artist.id} artist={artist} />
              ))}
            </section>
          </section>
        </div>
      </div>
    </main>
  );
}

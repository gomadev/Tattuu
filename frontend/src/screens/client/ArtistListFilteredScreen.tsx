import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { ArtistCard } from '../../components/ArtistCard';
import { Chip } from '../../components/Chip';
import { SearchBar } from '../../components/SearchBar';
import { artistsMock } from '../../data/artists';

const activeFilters = ['Blackwork', 'Fineline'];

export function ArtistListFilteredScreen() {
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const artists = useMemo(() => {
    const query = search.toLowerCase().trim();

    return artistsMock.filter((artist) => {
      const matchesFilter = activeFilters.some((style) => artist.styles.includes(style));
      const matchesQuery =
        !query ||
        artist.name.toLowerCase().includes(query) ||
        artist.shortDescription.toLowerCase().includes(query);

      return matchesFilter && matchesQuery;
    });
  }, [search]);

  return (
    <main className="screen screen--light">
      <div className="page-frame">
        <div className="client-layout">
          <aside className="client-sidebar">
            <div className="client-sidebar-card">
              <img src="/tattoo_logo_light.png" alt="Tattoo" className="logo-top" />
              <h2>Filtros aplicados</h2>
              <p>Esta tela mostra a mesma listagem com chips ativos e resultados recalculados.</p>
            </div>

            <div className="client-sidebar-card">
              <h2>Filtros ativos</h2>
              <div className="chip-row">
                {activeFilters.map((filter) => (
                  <Chip key={filter} label={filter} selected />
                ))}
              </div>
            </div>

            <div className="client-sidebar-card">
              <button type="button" className="secondary-button" onClick={() => navigate('/client/artists')}>
                Voltar para lista
              </button>
            </div>
          </aside>

          <section className="client-main">
            <div className="client-toolbar">
              <div className="client-toolbar-title">
                <strong>Resultados filtrados</strong>
                <span>{artists.length} artista(s) dentro dos critérios</span>
              </div>
              <SearchBar value={search} placeholder="Buscar artistas filtrados" onChange={setSearch} />
              <div className="chip-row">
                {activeFilters.map((filter) => (
                  <Chip key={filter} label={filter} selected />
                ))}
              </div>
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

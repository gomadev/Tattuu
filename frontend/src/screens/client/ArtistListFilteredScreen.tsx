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
      <header className="list-header">
        <img src="/tattoo_logo_light.png" alt="Tattoo" className="logo-top" />
        <SearchBar value={search} placeholder="Buscar artistas filtrados" onChange={setSearch} />
        <div className="chip-row">
          {activeFilters.map((filter) => (
            <Chip key={filter} label={filter} selected />
          ))}
        </div>
      </header>

      <section className="list-content">
        {artists.map((artist) => (
          <ArtistCard key={artist.id} artist={artist} />
        ))}
      </section>

      <footer className="screen-footer-row">
        <button type="button" className="secondary-button" onClick={() => navigate('/client/artists')}>
          Voltar para lista
        </button>
      </footer>
    </main>
  );
}

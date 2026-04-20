import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { ArtistCard } from '../../components/ArtistCard';
import { SearchBar } from '../../components/SearchBar';
import { artistsMock } from '../../data/artists';

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
      <header className="list-header">
        <img src="/tattoo_logo_light.png" alt="Tattoo" className="logo-top" />
        <SearchBar value={search} placeholder="Busque por nome ou estilo" onChange={setSearch} />
      </header>

      <section className="list-content">
        {artists.map((artist) => (
          <ArtistCard key={artist.id} artist={artist} />
        ))}
      </section>

      <footer className="screen-footer-row">
        <button type="button" className="secondary-button" onClick={() => navigate('/client/filtered')}>
          Ver versão filtrada
        </button>
        <button type="button" className="secondary-button" onClick={() => navigate('/client/empty')}>
          Simular sem resultados
        </button>
      </footer>
    </main>
  );
}

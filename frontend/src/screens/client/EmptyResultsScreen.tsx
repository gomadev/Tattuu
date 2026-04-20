import { useNavigate } from 'react-router-dom';

import { SearchBar } from '../../components/SearchBar';

export function EmptyResultsScreen() {
  const navigate = useNavigate();

  return (
    <main className="screen screen--light empty-screen">
      <header className="list-header">
        <img src="/tattoo_logo_light.png" alt="Tattoo" className="logo-top" />
        <SearchBar value="" placeholder="Buscar artistas" onChange={() => undefined} />
      </header>

      <section className="empty-state">
        <p>
          Você chegou ao fim dos resultados. Ajuste os filtros para encontrar mais artistas.
        </p>
      </section>

      <footer className="empty-footer">
        <img src="/tattoo_logo_dark.png" alt="Tattoo" className="logo-bottom" />
        <button type="button" className="secondary-button" onClick={() => navigate('/client/artists')}>
          Voltar para listagem
        </button>
      </footer>
    </main>
  );
}

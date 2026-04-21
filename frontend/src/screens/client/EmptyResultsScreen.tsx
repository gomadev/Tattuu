import { useNavigate } from 'react-router-dom';

import { SearchBar } from '../../components/SearchBar';

export function EmptyResultsScreen() {
  const navigate = useNavigate();

  return (
    <main className="screen screen--light empty-screen">
      <div className="page-frame">
        <div className="client-layout">
          <aside className="client-sidebar">
            <div className="client-sidebar-card">
              <img src="/tattoo_logo_light.png" alt="Tattoo" className="logo-top" />
              <h2>Sem resultados agora</h2>
              <p>A lógica da busca continua ativa; aqui só não há cards compatíveis com o filtro atual.</p>
            </div>

            <div className="client-sidebar-card">
              <button type="button" className="secondary-button" onClick={() => navigate('/client/artists')}>
                Voltar para listagem
              </button>
            </div>
          </aside>

          <section className="client-main">
            <div className="client-toolbar">
              <div className="client-toolbar-title">
                <strong>Busca vazia</strong>
                <span>Você chegou ao fim dos resultados</span>
              </div>
              <SearchBar value="" placeholder="Buscar artistas" onChange={() => undefined} />
            </div>

            <section className="empty-state">
              <p>
                Você chegou ao fim dos resultados. Ajuste os filtros para encontrar mais artistas.
              </p>
            </section>

            <footer className="empty-footer">
              <img src="/tattoo_logo_dark.png" alt="Tattoo" className="logo-bottom" />
            </footer>
          </section>
        </div>
      </div>
    </main>
  );
}

import { useNavigate } from 'react-router-dom';

export function RoleSelectorScreen() {
  const navigate = useNavigate();

  return (
    <main className="screen screen--dark screen--center gap-lg">
      <button type="button" className="image-button" onClick={() => navigate('/client/artists')}>
        <img src="/buttons_cliente.png" alt="Quero me Tatuar" />
      </button>
      <button type="button" className="image-button" onClick={() => navigate('/artist/splash')}>
        <img src="/buttons_tatuador.png" alt="Sou Tatuador" />
      </button>
    </main>
  );
}

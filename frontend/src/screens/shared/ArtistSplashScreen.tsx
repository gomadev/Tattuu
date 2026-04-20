import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function ArtistSplashScreen() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => navigate('/artist/onboarding/name'), 1200);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <main className="screen screen--light screen--center">
      <img src="/tattoo_logo_dark.png" alt="Perfil do Tatuador" className="logo-splash" />
    </main>
  );
}

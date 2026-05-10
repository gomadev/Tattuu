import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function ArtistSplashScreen() {
  const navigate = useNavigate();
  const [isLeaving, setIsLeaving] = useState(false);

  useEffect(() => {
    const leaveTimer = setTimeout(() => setIsLeaving(true), 850);
    const navigateTimer = setTimeout(() => navigate('/artist/onboarding/name'), 1200);

    return () => {
      clearTimeout(leaveTimer);
      clearTimeout(navigateTimer);
    };
  }, [navigate]);

  return (
    <main className={`screen screen--dark screen--center screen--fade ${isLeaving ? 'screen--fade-out' : 'screen--fade-in'}`}>
      <img src="/tattoo_logo_dark.png" alt="Perfil do Tatuador" className="logo-splash" />
    </main>
  );
}

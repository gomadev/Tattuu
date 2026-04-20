import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function SplashScreen() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => navigate('/role'), 1200);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <main className="screen screen--dark screen--center">
      <img src="/tattoo_invertido.png" alt="Tattoo" className="logo-splash" />
    </main>
  );
}

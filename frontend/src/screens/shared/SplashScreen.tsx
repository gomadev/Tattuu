import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

export function SplashScreen() {
  const navigate = useNavigate();
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const audio = audioRef.current;

    const primeAudio = () => {
      if (!audio) {
        return;
      }

      audio.muted = true;
      audio.volume = 0.35;
      audio.currentTime = 0;
      void audio.play().catch(() => undefined);
    };

    const enableAudio = () => {
      if (!audio) {
        return;
      }

      audio.muted = false;
      audio.volume = 0.35;

      if (audio.paused) {
        void audio.play().catch(() => undefined);
      }
    };

    primeAudio();
    const autoEnableTimer = setTimeout(enableAudio, 220);

    const handleInteraction = () => {
      enableAudio();
    };

    window.addEventListener('pointerdown', handleInteraction, { once: true });
    window.addEventListener('touchstart', handleInteraction, { once: true });
    window.addEventListener('keydown', handleInteraction, { once: true });

    const timer = setTimeout(() => navigate('/role'), 10000);

    return () => {
      clearTimeout(timer);
      clearTimeout(autoEnableTimer);
      window.removeEventListener('pointerdown', handleInteraction);
      window.removeEventListener('touchstart', handleInteraction);
      window.removeEventListener('keydown', handleInteraction);
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
        audio.muted = true;
      }
    };
  }, [navigate]);

  return (
    <main className="screen screen--dark splash-screen">
      <img src="/tattoo_logo_dark.png" alt="Tattoo" className="logo-splash" />
      <audio ref={audioRef} src="/tattoo_machine.mp3" autoPlay loop preload="auto" />
    </main>
  );
}

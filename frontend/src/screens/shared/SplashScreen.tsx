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
      <div className="splash-canvas" aria-hidden="true">
        <div className="splash-vignette" />
        <svg className="tattoo-stroke" viewBox="0 0 1000 1000" preserveAspectRatio="none">
          <path className="tattoo-stroke-primary tattoo-stroke-primary--one" d="M-80 160 C 130 -30, 330 320, 560 150 S 880 -20, 1120 180" />
          <path className="tattoo-stroke-primary tattoo-stroke-primary--two" d="M-100 500 C 120 310, 310 720, 570 500 S 910 290, 1130 530" />
          <path className="tattoo-stroke-primary tattoo-stroke-primary--three" d="M-80 860 C 140 650, 330 1040, 590 850 S 900 660, 1120 860" />
          <path className="tattoo-stroke-secondary tattoo-stroke-secondary--one" d="M20 80 C 230 230, 430 -20, 640 130 S 910 240, 1080 80" />
          <path className="tattoo-stroke-secondary tattoo-stroke-secondary--two" d="M-40 310 C 180 220, 360 430, 580 320 S 900 210, 1120 320" />
          <path className="tattoo-stroke-secondary tattoo-stroke-secondary--three" d="M0 690 C 220 560, 400 850, 640 700 S 930 560, 1140 700" />
          <path className="tattoo-stroke-secondary tattoo-stroke-secondary--four" d="M110 940 C 320 790, 520 1050, 730 920 S 960 780, 1120 940" />
        </svg>
      </div>

      <div className="splash-brand">
        <img src="/tattoo_logo_dark.png" alt="Tattoo" className="logo-splash" />
      </div>

      <div className="splash-loading" aria-live="polite" aria-label="Carregando">
        <span className="splash-spinner" />
      </div>

      <audio ref={audioRef} src="/tattoo_machine.mp3" autoPlay loop preload="auto" />
    </main>
  );
}

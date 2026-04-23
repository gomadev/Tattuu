import type { ArtistProfile } from '../types/artist';
import { Chip } from './Chip';

interface ArtistCardProps {
  artist: ArtistProfile;
}

export function ArtistCard({ artist }: ArtistCardProps) {
  const initials = artist.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase();

  return (
    <article className="artist-card">
      {artist.portfolioImage && (
        <div className="artist-card-image">
          <img src={artist.portfolioImage} alt={artist.name} />
        </div>
      )}

      <div className="artist-card-body">
        <div className="artist-card-header">
          <div className="artist-avatar">{initials}</div>
          <div className="artist-card-meta">
            <h3>{artist.name}</h3>
            <a href="#" className="artist-link" aria-label={`Abrir perfil de ${artist.name}`}>
              {artist.profileUrl}
            </a>
          </div>
        </div>

        <p className="artist-description">{artist.shortDescription}</p>

        <div className="artist-styles">
          {artist.styles.map((style) => (
            <Chip key={style} label={style} />
          ))}
        </div>

        <button type="button" className="artist-view-button">
          Ver Perfil Completo →
        </button>
      </div>
    </article>
  );
}

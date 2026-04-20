import type { ArtistProfile } from '../types/artist';
import { Chip } from './Chip';

interface ArtistCardProps {
  artist: ArtistProfile;
}

export function ArtistCard({ artist }: ArtistCardProps) {
  return (
    <article className="artist-card">
      <h3>{artist.name}</h3>
      <a href="#" className="artist-link" aria-label={`Abrir perfil de ${artist.name}`}>
        {artist.profileUrl}
      </a>
      <p>{artist.shortDescription}</p>
      <div className="chip-row">
        {artist.styles.map((style) => (
          <Chip key={style} label={style} />
        ))}
      </div>
    </article>
  );
}

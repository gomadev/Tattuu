export interface ArtistProfile {
  id: string;
  name: string;
  profileUrl: string;
  shortDescription: string;
  portfolioImage?: string;
  handle?: string;
  bio: string;
  styles: string[];
}

export interface ArtistFilters {
  query: string;
  styles: string[];
}

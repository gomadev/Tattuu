export interface ArtistProfile {
  id: string;
  name: string;
  profileUrl: string;
  shortDescription: string;
  styles: string[];
}

export interface ArtistFilters {
  query: string;
  styles: string[];
}

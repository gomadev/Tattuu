import type { ArtistProfile } from '../types/artist';

export const artistsMock: ArtistProfile[] = [
  {
    id: '1',
    name: 'Luna Ink',
    profileUrl: '@luna.ink',
    shortDescription: 'Especialista em blackwork e composição autoral com linhas limpas.',
    portfolioImage: 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=400&h=300&fit=crop',
    handle: '@luna.ink',
    bio: 'Especialista em blackwork e composição autoral com linhas limpas.',
    styles: ['Blackwork', 'Fineline'],
  },
  {
    id: '2',
    name: 'Rafael Ortega',
    profileUrl: '@rafael.realismo',
    shortDescription: 'Foco em realismo preto e cinza, retratos e peças de grande escala.',
    portfolioImage: 'https://images.unsplash.com/photo-1578482326878-e551d89a42dd?w=400&h=300&fit=crop',
    handle: '@rafael.realismo',
    bio: 'Foco em realismo preto e cinza, retratos e peças de grande escala.',
    styles: ['Realismo', 'Blackwork'],
  },
  {
    id: '3',
    name: 'Maya Color',
    profileUrl: '@maya.aquarela',
    shortDescription: 'Aquarela vibrante com traço leve e composição orgânica.',
    portfolioImage: 'https://images.unsplash.com/photo-1585072100629-903b34c11d9b?w=400&h=300&fit=crop',
    handle: '@maya.aquarela',
    bio: 'Aquarela vibrante com traço leve e composição orgânica.',
    styles: ['Aquarela', 'Realismo'],
  },
  {
    id: '4',
    name: 'Nico Geometry',
    profileUrl: '@nico.geo',
    shortDescription: 'Geometria, mandalas e projetos com precisão milimétrica.',
    portfolioImage: 'https://images.unsplash.com/photo-1598412522097-4c82b5db9d20?w=400&h=300&fit=crop',
    handle: '@nico.geo',
    bio: 'Geometria, mandalas e projetos com precisão milimétrica.',
    styles: ['Blackwork', 'Fineline'],
  },
];

export const styleOptions = [
  'Blackwork',
  'Realismo',
  'Aquarela',
  'Geométrico',
  'Old School',
  'Neo Tradicional',
  'Fineline',
  'Tribal',
];

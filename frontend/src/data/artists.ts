import type { ArtistProfile } from '../types/artist';

export const artistsMock: ArtistProfile[] = [
  {
    id: '1',
    name: 'Luna Ink',
    profileUrl: '@luna.ink',
    shortDescription: 'Especialista em blackwork e composição autoral com linhas limpas.',
    styles: ['Blackwork', 'Fineline'],
  },
  {
    id: '2',
    name: 'Rafael Ortega',
    profileUrl: '@rafael.realismo',
    shortDescription: 'Foco em realismo preto e cinza, retratos e peças de grande escala.',
    styles: ['Realismo', 'Blackwork'],
  },
  {
    id: '3',
    name: 'Maya Color',
    profileUrl: '@maya.aquarela',
    shortDescription: 'Aquarela vibrante com traço leve e composição orgânica.',
    styles: ['Aquarela', 'Neo Tradicional'],
  },
  {
    id: '4',
    name: 'Nico Geometry',
    profileUrl: '@nico.geo',
    shortDescription: 'Geometria, mandalas e projetos com precisão milimétrica.',
    styles: ['Geométrico', 'Tribal'],
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

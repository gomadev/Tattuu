export interface OnboardingData {
  fullName: string;
  bio: string;
  city: string;
  neighborhood: string;
  portfolioImages: string[];
  styles: string[];
  pricingModel: 'por-hora' | 'por-peca' | 'a-combinar' | '';
  pricingNotes: string;
}

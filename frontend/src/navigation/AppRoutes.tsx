import { Navigate, Route, Routes } from 'react-router-dom';

import { ArtistListFilteredScreen } from '../screens/client/ArtistListFilteredScreen';
import { ArtistListScreen } from '../screens/client/ArtistListScreen';
import { EmptyResultsScreen } from '../screens/client/EmptyResultsScreen';
import { OnboardingBioScreen } from '../screens/onboarding/OnboardingBioScreen';
import { OnboardingLocationScreen } from '../screens/onboarding/OnboardingLocationScreen';
import { OnboardingNameScreen } from '../screens/onboarding/OnboardingNameScreen';
import { OnboardingPaymentScreen } from '../screens/onboarding/OnboardingPaymentScreen';
import { OnboardingPortfolioScreen } from '../screens/onboarding/OnboardingPortfolioScreen';
import { OnboardingTagsScreen } from '../screens/onboarding/OnboardingTagsScreen';
import { ArtistSplashScreen } from '../screens/shared/ArtistSplashScreen';
import { RoleSelectorScreen } from '../screens/shared/RoleSelectorScreen';
import { SplashScreen } from '../screens/shared/SplashScreen';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<SplashScreen />} />
      <Route path="/role" element={<RoleSelectorScreen />} />

      <Route path="/client/artists" element={<ArtistListScreen />} />
      <Route path="/client/filtered" element={<ArtistListFilteredScreen />} />
      <Route path="/client/empty" element={<EmptyResultsScreen />} />

      <Route path="/artist/splash" element={<ArtistSplashScreen />} />
      <Route path="/artist/onboarding/name" element={<OnboardingNameScreen />} />
      <Route path="/artist/onboarding/bio" element={<OnboardingBioScreen />} />
      <Route path="/artist/onboarding/location" element={<OnboardingLocationScreen />} />
      <Route path="/artist/onboarding/portfolio" element={<OnboardingPortfolioScreen />} />
      <Route path="/artist/onboarding/tags" element={<OnboardingTagsScreen />} />
      <Route path="/artist/onboarding/payment" element={<OnboardingPaymentScreen />} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

import { createContext, useContext, useMemo, useState, type PropsWithChildren } from 'react';

import type { OnboardingData } from '../types/onboarding';

interface OnboardingContextValue {
  data: OnboardingData;
  updateData: (nextData: Partial<OnboardingData>) => void;
  resetData: () => void;
}

const initialOnboardingData: OnboardingData = {
  fullName: '',
  bio: '',
  city: '',
  neighborhood: '',
  portfolioImages: [],
  styles: [],
  pricingModel: '',
  pricingNotes: '',
};

const OnboardingContext = createContext<OnboardingContextValue | null>(null);

export function OnboardingProvider({ children }: PropsWithChildren) {
  const [data, setData] = useState<OnboardingData>(initialOnboardingData);

  function updateData(nextData: Partial<OnboardingData>) {
    setData((current) => ({ ...current, ...nextData }));
  }

  function resetData() {
    setData(initialOnboardingData);
  }

  const value = useMemo(
    () => ({ data, updateData, resetData }),
    [data],
  );

  return <OnboardingContext.Provider value={value}>{children}</OnboardingContext.Provider>;
}

export function useOnboarding() {
  const context = useContext(OnboardingContext);

  if (!context) {
    throw new Error('useOnboarding must be used within OnboardingProvider');
  }

  return context;
}

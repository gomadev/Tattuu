import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingBioScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Descreva seu ' },
        { text: 'estilo', highlight: true },
        { text: ', ' },
        { text: 'experiência', highlight: true },
        { text: ' e o que torna seu trabalho ' },
        { text: 'único', highlight: true },
        { text: '.' },
      ]}
      subtitleInputValue={data.bio}
      subtitleInputPlaceholder="Só 300 caracteres, mas relaxa... depois dá pra cobrir."
      subtitleInputMaxLength={300}
      subtitleInputMultiline
      subtitleInputAriaLabel="Bio do artista"
      onSubtitleInputChange={(value) => updateData({ bio: value })}
      footerLabel="Próximo"
      onNext={() => navigate('/artist/onboarding/location')}
    />
  );
}

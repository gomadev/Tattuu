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
      footerLabel="Próximo"
      onNext={() => navigate('/artist/onboarding/location')}
      asideTitle="Etapa 2 de 5"
      asideText="Use a bio para destacar experiência, técnica e personalidade."
      asideItems={['Tom autoral', 'Experiência prática', 'Diferencial do estúdio']}
    >
      <textarea
        className="text-area"
        value={data.bio}
        placeholder="Fale sobre seu estilo e experiência"
        onChange={(event) => updateData({ bio: event.target.value })}
      />
    </OnboardingLayout>
  );
}

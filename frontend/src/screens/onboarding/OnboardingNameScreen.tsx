import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

const MAX_NAME_LENGTH = 300;

export function OnboardingNameScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  function handleNext() {
    if (!data.fullName.trim()) {
      return;
    }

    navigate('/artist/onboarding/bio');
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Conte-nos um pouco ' },
        { text: 'sobre você!', highlight: true },
      ]}
      subtitleInputValue={data.fullName}
      subtitleInputPlaceholder="Seu nome artístico..."
      subtitleInputMaxLength={MAX_NAME_LENGTH}
      subtitleInputAriaLabel="Nome artístico"
      onSubtitleInputChange={(value) => updateData({ fullName: value })}
      footerLabel="Próximo"
      onNext={handleNext}
      footerExtra={<span className="counter">{data.fullName.length}/{MAX_NAME_LENGTH}</span>}
    />
  );
}

import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingLocationScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();
  const locationValue = [data.city, data.neighborhood].filter(Boolean).join(' - ');

  function handleLocationChange(value: string) {
    const [city = '', neighborhood = ''] = value.split('-').map((part) => part.trim());
    updateData({ city, neighborhood });
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Informe a ' },
        { text: 'cidade', highlight: true },
        { text: ' e o ' },
        { text: 'bairro', highlight: true },
        { text: ' onde você atende.' },
      ]}
      subtitleInputValue={locationValue}
      subtitleInputPlaceholder="Pode colocar certinho… mas vão pedir no WhatsApp de qualquer forma."
      subtitleInputAriaLabel="Cidade e bairro"
      onSubtitleInputChange={handleLocationChange}
      footerLabel="Próximo"
      onNext={() => navigate('/artist/onboarding/portfolio')}
    />
  );
}

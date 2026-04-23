import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingPaymentScreen() {
  const { data, updateData, resetData } = useOnboarding();
  const navigate = useNavigate();

  function finishOnboarding() {
    resetData();
    navigate('/client/artists');
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Como você ' },
        { text: 'cobra ', highlight: true },
        { text: 'pelo seu trabalho?' },
      ]}
      subtitleInputValue={data.pricingNotes}
      subtitleInputPlaceholder="Pix não dói. A tatuagem talvez.."
      subtitleInputAriaLabel="Informações de pagamento"
      onSubtitleInputChange={(value) => updateData({ pricingNotes: value })}
      footerLabel="Finalizar"
      onNext={finishOnboarding}
    />
  );
}

import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

const paymentOptions = [
  { id: 'por-hora', label: 'Por hora' },
  { id: 'por-peca', label: 'Por peça' },
  { id: 'a-combinar', label: 'A combinar' },
] as const;

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
        { text: 'cobra', highlight: true },
        { text: ' pelo seu trabalho?' },
      ]}
      footerLabel="Finalizar"
      onNext={finishOnboarding}
    >
      <div className="payment-grid">
        {paymentOptions.map((option) => (
          <button
            type="button"
            key={option.id}
            className={`payment-card ${data.pricingModel === option.id ? 'payment-card--active' : ''}`}
            onClick={() => updateData({ pricingModel: option.id })}
          >
            {option.label}
          </button>
        ))}
      </div>

      <textarea
        className="text-area"
        value={data.pricingNotes}
        placeholder="Informações adicionais (opcional)"
        onChange={(event) => updateData({ pricingNotes: event.target.value })}
      />
    </OnboardingLayout>
  );
}

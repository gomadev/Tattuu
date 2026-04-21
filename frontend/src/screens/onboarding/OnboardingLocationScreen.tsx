import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingLocationScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Informe a ' },
        { text: 'cidade', highlight: true },
        { text: ' e o ' },
        { text: 'bairro', highlight: true },
        { text: ' onde você atende.' },
      ]}
      subtitle="Você só precisa informar sua base principal, mas pode receber clientes de qualquer forma."
      footerLabel="Próximo"
      onNext={() => navigate('/artist/onboarding/portfolio')}
      asideTitle="Etapa 3 de 5"
      asideText="Informar localização ajuda a segmentar melhor o atendimento e a busca local."
      asideItems={['Cidade', 'Bairro', 'Abrangência de atendimento']}
    >
      <div className="field-column">
        <input
          className="text-input"
          value={data.city}
          placeholder="Cidade"
          onChange={(event) => updateData({ city: event.target.value })}
        />
        <input
          className="text-input"
          value={data.neighborhood}
          placeholder="Bairro"
          onChange={(event) => updateData({ neighborhood: event.target.value })}
        />
      </div>
    </OnboardingLayout>
  );
}

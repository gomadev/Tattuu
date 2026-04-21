import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

const MAX_NAME_LENGTH = 300;

export function OnboardingNameScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Conte-nos um pouco ' },
        { text: 'sobre você', highlight: true },
      ]}
      footerLabel="Próximo"
      onNext={() => navigate('/artist/onboarding/bio')}
      asideTitle="Etapa 1 de 5"
      asideText="Um layout web ajuda a distribuir a informação de forma mais confortável em telas grandes."
      asideItems={['Cadastro guiado', 'Campos com feedback', 'Pronto para desktop']}
      footerExtra={<span className="counter">{data.fullName.length}/{MAX_NAME_LENGTH}</span>}
    >
      <input
        className="text-input"
        value={data.fullName}
        maxLength={MAX_NAME_LENGTH}
        placeholder="Nome completo"
        onChange={(event) => updateData({ fullName: event.target.value })}
      />
    </OnboardingLayout>
  );
}

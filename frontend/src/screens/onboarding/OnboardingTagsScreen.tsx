import { useNavigate } from 'react-router-dom';

import { Chip } from '../../components/Chip';
import { OnboardingLayout } from '../../components/OnboardingLayout';
import { styleOptions } from '../../data/artists';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingTagsScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  function toggleStyle(style: string) {
    const next = (() => {
      const current = data.styles;
      if (current.includes(style)) {
        return current.filter((item) => item !== style);
      }

      return [...current, style];
    })();

    updateData({ styles: next });
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Quais ' },
        { text: 'estilos', highlight: true },
        { text: ' você trabalha?' },
      ]}
      footerLabel="Tudo certo, esses são seus estilos?"
      onNext={() => navigate('/artist/onboarding/payment')}
    >
      <div className="chip-grid">
        {styleOptions.map((style) => (
          <Chip
            key={style}
            label={style}
              selected={data.styles.includes(style)}
            onClick={() => toggleStyle(style)}
          />
        ))}
      </div>
    </OnboardingLayout>
  );
}

import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingPortfolioScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  function addPlaceholderImage() {
    const index = data.portfolioImages.length;
    const next = [...data.portfolioImages];
    next[index] = `/resumo.png?slot=${index}`;
    updateData({ portfolioImages: next });
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Upload de ' },
        { text: 'fotos', highlight: true },
        { text: ' do seu trabalho' },
      ]}
      subtitle="Se a tattoo é linda, deixa a gente ver também."
      footerLabel="Tudo certo, esse é seu portfólio?"
      onNext={() => navigate('/artist/onboarding/tags')}
    >
      <div className="portfolio-stage">
        <button
          type="button"
          className="portfolio-add-button"
          onClick={addPlaceholderImage}
          aria-label="Adicionar foto ao portfólio"
        >
          +
        </button>
      </div>
    </OnboardingLayout>
  );
}

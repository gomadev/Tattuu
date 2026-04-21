import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingPortfolioScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();

  const portfolio = Array.from({ length: 4 }).map((_, index) => data.portfolioImages[index] ?? '');

  function addPlaceholderImage(index: number) {
    const next = [...data.portfolioImages];
    next[index] = `/resumo.png?slot=${index}`;
    updateData({ portfolioImages: next });
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Agora é hora de deixar a ' },
        { text: 'agulha', highlight: true },
        { text: ' falar.' },
      ]}
      subtitle="Se a tattoo é linda, deixa a gente ver também."
      footerLabel="Tudo certo, esse é seu portfólio?"
      onNext={() => navigate('/artist/onboarding/tags')}
      asideTitle="Etapa 4 de 5"
      asideText="O grid de imagens funciona melhor quando há respiro visual e organização em desktop."
      asideItems={['Upload em grade', 'Preview imediato', 'Portfólio visual']}
    >
      <div className="portfolio-grid">
        {portfolio.map((item, index) => (
          <button
            type="button"
            key={index}
            className="portfolio-item"
            onClick={() => addPlaceholderImage(index)}
          >
            {item ? <img src={item} alt={`Portfólio ${index + 1}`} /> : <span>+ Adicionar</span>}
          </button>
        ))}
      </div>
    </OnboardingLayout>
  );
}

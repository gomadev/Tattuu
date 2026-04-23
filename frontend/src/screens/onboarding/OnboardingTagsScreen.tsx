import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { OnboardingLayout } from '../../components/OnboardingLayout';
import { useOnboarding } from '../../navigation/OnboardingContext';

export function OnboardingTagsScreen() {
  const { data, updateData } = useOnboarding();
  const navigate = useNavigate();
  const [newTag, setNewTag] = useState('');

  function addTag() {
    const tag = newTag.trim();
    if (!tag) {
      return;
    }

    const exists = data.styles.some((item) => item.toLowerCase() === tag.toLowerCase());
    if (exists) {
      setNewTag('');
      return;
    }

    updateData({ styles: [...data.styles, tag] });
    setNewTag('');
  }

  function removeTag(index: number) {
    updateData({ styles: data.styles.filter((_, itemIndex) => itemIndex !== index) });
  }

  function handleNext() {
    const cleanedTags = data.styles
      .map((tag) => tag.trim())
      .filter((tag) => tag.length > 0);

    updateData({ styles: cleanedTags });
    navigate('/artist/onboarding/payment');
  }

  return (
    <OnboardingLayout
      titleParts={[
        { text: 'Quais ' },
        { text: 'estilos', highlight: true },
        { text: ' você trabalha?' },
      ]}
      subtitle="Se o cliente pedir realismo e você faz tribal… melhor marcar certo."
      footerLabel="Próximo"
      onNext={handleNext}
    >
      <div className="onboarding-tags-stack">
        {data.styles.length > 0 && (
          <div className="onboarding-tags-list">
            {data.styles.map((tag, index) => (
              <span key={`${tag}-${index}`} className="onboarding-tag-pill">
                {tag}
                <button
                  type="button"
                  className="onboarding-tag-remove"
                  onClick={() => removeTag(index)}
                  aria-label={`Remover tag ${tag}`}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}

        <div className="onboarding-tag-entry">
          <input
            className="text-input onboarding-tag-input"
            value={newTag}
            placeholder="Digite uma tag"
            onChange={(event) => setNewTag(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                event.preventDefault();
                addTag();
              }
            }}
          />
          <button type="button" className="onboarding-tag-add" onClick={addTag}>
            +
          </button>
        </div>
      </div>
    </OnboardingLayout>
  );
}

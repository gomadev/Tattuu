import type { PropsWithChildren, ReactNode } from 'react';

interface HighlightPart {
  text: string;
  highlight?: boolean;
}

interface OnboardingLayoutProps {
  titleParts: HighlightPart[];
  subtitle?: string;
  subtitleInputValue?: string;
  subtitleInputPlaceholder?: string;
  subtitleInputMaxLength?: number;
  subtitleInputMultiline?: boolean;
  subtitleInputAriaLabel?: string;
  onSubtitleInputChange?: (value: string) => void;
  footerLabel: string;
  onNext?: () => void;
  footerExtra?: ReactNode;
  asideTitle?: string;
  asideText?: string;
  asideItems?: string[];
}

export function OnboardingLayout({
  titleParts,
  subtitle,
  subtitleInputValue,
  subtitleInputPlaceholder,
  subtitleInputMaxLength,
  subtitleInputMultiline,
  subtitleInputAriaLabel,
  onSubtitleInputChange,
  footerLabel,
  onNext,
  footerExtra,
  children,
}: PropsWithChildren<OnboardingLayoutProps>) {
  const hasSubtitleInput = typeof onSubtitleInputChange === 'function';

  return (
    <main className="onboarding-screen onboarding-flow-screen screen--fade screen--fade-in">
      <section className="onboarding-flow-content">
        <h1>
          {titleParts.map((part, index) => (
            <span key={`${part.text}-${index}`} className={part.highlight ? 'text-highlight' : ''}>
              {part.text}
            </span>
          ))}
        </h1>
        {hasSubtitleInput ? (
          subtitleInputMultiline ? (
            <textarea
              className="onboarding-subtitle onboarding-subtitle-input onboarding-subtitle-input--multiline"
              value={subtitleInputValue ?? ''}
              maxLength={subtitleInputMaxLength}
              placeholder={subtitleInputPlaceholder}
              aria-label={subtitleInputAriaLabel ?? subtitleInputPlaceholder ?? 'Digite aqui'}
              onChange={(event) => onSubtitleInputChange(event.target.value)}
            />
          ) : (
            <input
              className="onboarding-subtitle onboarding-subtitle-input"
              value={subtitleInputValue ?? ''}
              maxLength={subtitleInputMaxLength}
              placeholder={subtitleInputPlaceholder}
              aria-label={subtitleInputAriaLabel ?? subtitleInputPlaceholder ?? 'Digite aqui'}
              onChange={(event) => onSubtitleInputChange(event.target.value)}
            />
          )
        ) : subtitle ? (
          <p className="onboarding-subtitle">{subtitle}</p>
        ) : null}

        <div className="onboarding-body">{children}</div>

        <footer className="onboarding-footer onboarding-footer--minimal">
          {footerExtra}
          <button type="button" className="primary-button onboarding-flow-next" onClick={onNext}>
            {footerLabel}
          </button>
        </footer>
      </section>
    </main>
  );
}

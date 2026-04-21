import type { PropsWithChildren, ReactNode } from 'react';

interface HighlightPart {
  text: string;
  highlight?: boolean;
}

interface OnboardingLayoutProps {
  titleParts: HighlightPart[];
  subtitle?: string;
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
  footerLabel,
  onNext,
  footerExtra,
  asideTitle,
  asideText,
  asideItems,
  children,
}: PropsWithChildren<OnboardingLayoutProps>) {
  return (
    <main className="onboarding-screen">
      <section className="onboarding-content">
        <div className="onboarding-shell">
          <div className="onboarding-panel">
            <h1>
              {titleParts.map((part, index) => (
                <span key={`${part.text}-${index}`} className={part.highlight ? 'text-highlight' : ''}>
                  {part.text}
                </span>
              ))}
            </h1>
            {subtitle ? <p className="onboarding-subtitle">{subtitle}</p> : null}
            <div className="onboarding-body">{children}</div>
            <footer className="onboarding-footer">
              {footerExtra}
              <button type="button" className="primary-button" onClick={onNext}>
                {footerLabel}
              </button>
            </footer>
          </div>

          <aside className="onboarding-aside">
            <h3>{asideTitle ?? 'Resumo da etapa'}</h3>
            <p>
              {asideText ?? 'Preencha os dados ao lado para avançar no cadastro do tatuador.'}
            </p>
            {asideItems?.length ? (
              <ul>
                {asideItems.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            ) : null}
          </aside>
        </div>
      </section>
    </main>
  );
}

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
}

export function OnboardingLayout({
  titleParts,
  subtitle,
  footerLabel,
  onNext,
  footerExtra,
  children,
}: PropsWithChildren<OnboardingLayoutProps>) {
  return (
    <main className="onboarding-screen">
      <section className="onboarding-content">
        <h1>
          {titleParts.map((part, index) => (
            <span key={`${part.text}-${index}`} className={part.highlight ? 'text-highlight' : ''}>
              {part.text}
            </span>
          ))}
        </h1>
        {subtitle ? <p className="onboarding-subtitle">{subtitle}</p> : null}
        <div className="onboarding-body">{children}</div>
      </section>
      <footer className="onboarding-footer">
        {footerExtra}
        <button type="button" className="primary-button" onClick={onNext}>
          {footerLabel}
        </button>
      </footer>
    </main>
  );
}

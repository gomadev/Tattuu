import { BrowserRouter } from 'react-router-dom';

import { OnboardingProvider } from './navigation/OnboardingContext';
import { AppRoutes } from './navigation/AppRoutes';

function App() {
  return (
    <OnboardingProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </OnboardingProvider>
  );
}

export default App;

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import GlobalStateProvider from './app/GlobalStateProvider';
import { QueryClient, QueryClientProvider } from 'react-query';

import './assets/css/normalize.css'
import './assets/css/global.css'
import './assets/css/framework.css'
import App from './App';

const queryClient = new QueryClient();

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <GlobalStateProvider>
          <App />
        </GlobalStateProvider>
      </QueryClientProvider>
    </BrowserRouter>
  </React.StrictMode>
);


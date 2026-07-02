import { useState } from 'react';
import Landing from './components/Landing';
import Diagnostico from './components/Diagnostico';
import Dashboard from './components/Dashboard';

const API_URL = import.meta.env.VITE_API_URL || '';

function App() {
  const [currentStep, setCurrentStep] = useState('landing');
  const [userData, setUserData] = useState(null);
  const [diagnosticoData, setDiagnosticoData] = useState(null);

  const handleLogin = (data) => {
    setUserData(data);
    if (data.perfil.includes('Nacer')) {
      setCurrentStep('diagnostico');
    } else {
      setCurrentStep('diagnostico');
    }
  };

  const handleDiagnosticoComplete = (data) => {
    setDiagnosticoData(data);
    setCurrentStep('dashboard');
  };

  const handleReset = () => {
    setCurrentStep('landing');
    setUserData(null);
    setDiagnosticoData(null);
  };

  return (
    <div className="app-wrapper">
      {/* ── Header ──────────────────────────────────────────────────── */}
      <header className="app-header">
        <div className="container">
          <div className="header-brand">
            <div className="header-logo-icon">RI</div>
            <div>
              <div className="header-title">Ruta Integral de Apoyo Empresarial</div>
              <div className="header-subtitle">MinCIT · Prototipo Funcional</div>
            </div>
          </div>
          <div className="header-actions">
            {currentStep !== 'landing' && (
              <button className="btn btn-ghost" style={{ color: 'var(--color-gray-400)' }} onClick={handleReset}>
                Cerrar sesión
              </button>
            )}
          </div>
        </div>
      </header>

      {/* ── Main ────────────────────────────────────────────────────── */}
      <main style={{ flex: 1, padding: 'var(--space-8) 0' }}>
        <div className="container">
          {currentStep === 'landing' && (
            <Landing apiUrl={API_URL} onLogin={handleLogin} />
          )}
          {currentStep === 'diagnostico' && (
            <Diagnostico apiUrl={API_URL} userData={userData} onComplete={handleDiagnosticoComplete} />
          )}
          {currentStep === 'dashboard' && (
            <Dashboard userData={userData} diagnosticoData={diagnosticoData} onReset={handleReset} />
          )}
        </div>
      </main>

      {/* ── Footer ──────────────────────────────────────────────────── */}
      <footer className="app-footer">
        <div className="container">
          Prototipo funcional · Metodología <span>ArCo</span> · Ministerio de Comercio, Industria y Turismo · 2026
        </div>
      </footer>
    </div>
  );
}

export default App;

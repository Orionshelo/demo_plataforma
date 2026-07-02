import { useState } from 'react';

function Landing({ apiUrl, onLogin }) {
  const [authType, setAuthType] = useState('nit');
  const [identificador, setIdentificador] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!identificador.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${apiUrl}/api/auth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identificador, tipo: authType }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        onLogin({
          identificador,
          tipo: authType,
          perfil: data.perfil,
          datos: data.datos_basicos,
          mensaje: data.mensaje,
        });
      } else {
        setError(data.mensaje || 'Error al procesar la solicitud.');
      }
    } catch {
      setError('No se pudo conectar con el servidor. Verifique que el backend esté activo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-in" style={{ maxWidth: '580px', margin: '4vh auto 0' }}>
      {/* Hero */}
      <div className="section-header text-center" style={{ marginBottom: 'var(--space-10)' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: 'var(--space-3)' }}>
          Acceda a la oferta institucional del Estado
        </h1>
        <p style={{ maxWidth: '460px', margin: '0 auto' }}>
          Identifique su estadio empresarial y reciba recomendaciones personalizadas
          de programas del MinCIT, iNNpulsa, Bancóldex, ProColombia y Fontur.
        </p>
      </div>

      {/* Selector Track A / Track B */}
      <div className="grid-2 mb-6" style={{ gap: 'var(--space-4)' }}>
        <div
          className={`card card-interactive ${authType === 'cedula' ? 'selected' : ''}`}
          onClick={() => setAuthType('cedula')}
          style={{ padding: 'var(--space-5)', textAlign: 'center' }}
        >
          <div style={{ 
            width: '40px', height: '40px', borderRadius: 'var(--radius-sm)',
            background: 'var(--color-navy-800)', color: 'var(--text-inverse)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto var(--space-3)', fontSize: '0.875rem', fontWeight: '700'
          }}>A</div>
          <h3 style={{ marginBottom: 'var(--space-1)' }}>Nacer</h3>
          <p className="text-sm" style={{ marginBottom: 0 }}>
            Emprendedores sin formalización
          </p>
        </div>

        <div
          className={`card card-interactive ${authType === 'nit' ? 'selected' : ''}`}
          onClick={() => setAuthType('nit')}
          style={{ padding: 'var(--space-5)', textAlign: 'center' }}
        >
          <div style={{
            width: '40px', height: '40px', borderRadius: 'var(--radius-sm)',
            background: 'var(--color-gold-500)', color: 'var(--color-navy-900)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto var(--space-3)', fontSize: '0.875rem', fontWeight: '700'
          }}>B</div>
          <h3 style={{ marginBottom: 'var(--space-1)' }}>Consolidar / Crecer</h3>
          <p className="text-sm" style={{ marginBottom: 0 }}>
            Empresa constituida con NIT
          </p>
        </div>
      </div>

      {/* Form */}
      <div className="card card-elevated animate-in">
        {error && (
          <div className="alert alert-warning mb-6">
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="identificador">
              {authType === 'cedula' ? 'Número de documento de identidad' : 'NIT de la empresa'}
            </label>
            <input
              className="form-input"
              type="text"
              id="identificador"
              value={identificador}
              onChange={(e) => setIdentificador(e.target.value)}
              placeholder={authType === 'cedula' ? '1.234.567.890' : '900123456-1'}
              autoComplete="off"
            />
            {authType === 'nit' && (
              <p className="form-hint">
                NITs de prueba: 900123456-1 · 800987654-2 · 901234567-3
              </p>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-lg btn-block"
            disabled={loading || !identificador.trim()}
          >
            {loading ? 'Validando datos oficiales…' : 'Continuar al diagnóstico'}
          </button>
        </form>

        <p className="text-xs text-center mt-4" style={{ color: 'var(--text-muted)' }}>
          Al continuar, autoriza el tratamiento de datos conforme al habeas data inverso
          para consultar RUES, PILA y Superintendencia de Sociedades.
        </p>
      </div>
    </div>
  );
}

export default Landing;

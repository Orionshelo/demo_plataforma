function Dashboard({ userData, diagnosticoData, onReset }) {
  const matches = diagnosticoData?.matches || [];
  const nombre = userData?.datos?.nombre || 'Emprendedor';
  const perfil = diagnosticoData?.perfil_calculado || userData?.perfil || '—';
  const totalInstrumentos = diagnosticoData?.total_instrumentos || '—';

  const highMatches = matches.filter((m) => m.match_score >= 80);
  const medMatches = matches.filter((m) => m.match_score >= 60 && m.match_score < 80);

  return (
    <div className="animate-in">
      {/* Section header */}
      <div className="flex justify-between items-center mb-8">
        <div className="section-header" style={{ marginBottom: 0 }}>
          <h1>Oferta institucional recomendada</h1>
          <p style={{ marginBottom: 0 }}>
            Resultados del emparejamiento semántico con {totalInstrumentos} instrumentos ArCo vigentes 2026.
          </p>
        </div>
      </div>

      <div className="grid-sidebar">
        {/* ── Sidebar ──────────────────────────────────────────────── */}
        <div className="flex-col gap-6" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
          {/* Profile Card */}
          <div className="card">
            <h3 style={{ marginBottom: 'var(--space-4)', fontSize: '0.9375rem' }}>Perfil empresarial</h3>
            <div className="stat-row">
              <span className="stat-label">Razón social</span>
              <span className="stat-value">{nombre}</span>
            </div>
            {userData?.datos?.sector && (
              <div className="stat-row">
                <span className="stat-label">Sector</span>
                <span className="stat-value">{userData.datos.sector}</span>
              </div>
            )}
            {userData?.datos?.tamaño && (
              <div className="stat-row">
                <span className="stat-label">Tamaño</span>
                <span className="stat-value">{userData.datos.tamaño}</span>
              </div>
            )}
            {userData?.datos?.empleados && (
              <div className="stat-row">
                <span className="stat-label">Empleados</span>
                <span className="stat-value">{userData.datos.empleados}</span>
              </div>
            )}
            {userData?.datos?.departamento && (
              <div className="stat-row">
                <span className="stat-label">Departamento</span>
                <span className="stat-value">{userData.datos.departamento}</span>
              </div>
            )}
            <div className="mt-4">
              <span className="badge badge-navy">{perfil}</span>
            </div>
          </div>

          {/* Interoperability verification */}
          {userData?.tipo === 'nit' && (
            <div className="card" style={{ background: 'var(--color-gray-50)' }}>
              <h3 style={{ marginBottom: 'var(--space-4)', fontSize: '0.9375rem' }}>Interoperabilidad</h3>
              <div className="flex-col" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {['RUES (Registro Único Empresarial)', 'PILA (Planilla Integrada)', 'Supersociedades'].map((src) => (
                  <div key={src} className="flex items-center" style={{ gap: 'var(--space-3)' }}>
                    <div style={{
                      width: '8px', height: '8px', borderRadius: '50%',
                      background: 'var(--color-success)', flexShrink: 0,
                    }} />
                    <span className="text-sm">{src}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tracker */}
          <div className="card">
            <h3 style={{ marginBottom: 'var(--space-4)', fontSize: '0.9375rem' }}>Tracker de interacciones</h3>
            <div className="timeline-item">
              <div className="timeline-dot timeline-dot-active" />
              <div className="timeline-content">
                <div className="timeline-title">Autodiagnóstico completado</div>
                <div className="timeline-meta">Hoy · Radar de Madurez procesado</div>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-dot timeline-dot-active" />
              <div className="timeline-content">
                <div className="timeline-title">Ingreso al sistema</div>
                <div className="timeline-meta">Hoy · Datos oficiales validados</div>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-dot timeline-dot-pending" />
              <div className="timeline-content">
                <div className="timeline-title">Postulación a programa</div>
                <div className="timeline-meta">Pendiente</div>
              </div>
            </div>
          </div>

          {/* Summary stats */}
          <div className="card" style={{ background: 'var(--color-navy-900)', color: 'var(--text-inverse)' }}>
            <h3 style={{ color: 'var(--color-gold-400)', marginBottom: 'var(--space-4)', fontSize: '0.9375rem' }}>
              Resumen del emparejamiento
            </h3>
            <div style={{ display: 'flex', gap: 'var(--space-6)' }}>
              <div>
                <div style={{ fontSize: '1.75rem', fontWeight: '800' }}>{matches.length}</div>
                <div className="text-xs" style={{ color: 'var(--color-gray-400)' }}>Programas compatibles</div>
              </div>
              <div>
                <div style={{ fontSize: '1.75rem', fontWeight: '800', color: 'var(--color-gold-400)' }}>
                  {highMatches.length}
                </div>
                <div className="text-xs" style={{ color: 'var(--color-gray-400)' }}>Match ≥ 80%</div>
              </div>
            </div>
          </div>
        </div>

        {/* ── Main content: Matches ────────────────────────────────── */}
        <div>
          {/* High matches */}
          {highMatches.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center mb-4" style={{ gap: 'var(--space-3)' }}>
                <h3 style={{ marginBottom: 0 }}>Alta coincidencia</h3>
                <span className="badge badge-success">{highMatches.length} programas</span>
              </div>
              <div className="flex-col stagger" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
                {highMatches.map((m, i) => (
                  <MatchCard key={i} match={m} />
                ))}
              </div>
            </div>
          )}

          {/* Medium matches */}
          {medMatches.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center mb-4" style={{ gap: 'var(--space-3)' }}>
                <h3 style={{ marginBottom: 0 }}>Coincidencia media</h3>
                <span className="badge badge-warning">{medMatches.length} programas</span>
              </div>
              <div className="flex-col stagger" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
                {medMatches.map((m, i) => (
                  <MatchCard key={i} match={m} />
                ))}
              </div>
            </div>
          )}

          {matches.length === 0 && (
            <div className="card text-center" style={{ padding: 'var(--space-12)' }}>
              <p>No se encontraron programas con un match superior al 60% en este momento.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


/* ── Match Card sub-component ──────────────────────────────────────── */
function MatchCard({ match }) {
  const { programa, match_score } = match;
  const scoreClass = match_score >= 80 ? 'score-high' : match_score >= 70 ? 'score-medium' : 'score-low';
  const scoreColor = match_score >= 80 ? 'var(--color-success)' : match_score >= 70 ? 'var(--color-gold-500)' : 'var(--color-warning)';

  return (
    <div className="card animate-in" style={{ padding: 'var(--space-5) var(--space-6)' }}>
      <div className="flex justify-between items-center" style={{ gap: 'var(--space-6)' }}>
        {/* Left: Info */}
        <div className="flex-1">
          <div className="flex items-center mb-2" style={{ gap: 'var(--space-2)' }}>
            <span className="badge badge-outline">{programa.entidad}</span>
            <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{programa.id}</span>
          </div>
          <h3 style={{ marginBottom: 'var(--space-2)', fontSize: '1.05rem' }}>{programa.nombre}</h3>
          <p className="text-sm" style={{ marginBottom: 'var(--space-3)' }}>{programa.descripcion}</p>

          {/* Tags */}
          <div>
            {programa.objetivos?.map((obj, i) => (
              <span key={i} className="tag">{obj}</span>
            ))}
            {programa.apoyos?.map((ap, i) => (
              <span key={`a-${i}`} className="tag" style={{ background: 'var(--color-info-light)', color: 'var(--color-info)' }}>
                {ap}
              </span>
            ))}
          </div>
        </div>

        {/* Right: Score */}
        <div className="match-score">
          <div className="match-score-value" style={{ color: scoreColor }}>{match_score}%</div>
          <div className="match-score-label">Match</div>
          <div className="score-bar" style={{ width: '56px' }}>
            <div className={`score-bar-fill ${scoreClass}`} style={{ width: `${match_score}%` }} />
          </div>
        </div>
      </div>

      <div className="divider" style={{ margin: 'var(--space-4) 0' }} />
      <button className="btn btn-primary btn-sm btn-block">
        Aplicar — Radicación virtual
      </button>
    </div>
  );
}

export default Dashboard;

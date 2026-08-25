import { useState } from 'react';

/** Cupos por instrumento: dato no disponible en la base ArCo, se simula. */
const CUPOS_SIMULADOS = 30;

/**
 * Paso 4 – Ventana de Aplicación
 * Muestra la información de la convocatoria seleccionada en el dashboard y
 * los datos de la empresa asociada al NIT ingresado. Incluye un botón de
 * acción que muestra un mensaje de éxito al aplicar.
 */
function ApplyStep({ userData, programa, onReset }) {
  const [applied, setApplied] = useState(false);

  const handleApply = () => {
    setApplied(true);
  };

  const datos = userData?.datos || {};
  const nit = userData?.identificador || datos?.nit || 'NIT no disponible';

  const objetivos = (programa?.objetivos || []).filter((o) => o && o !== '—');
  const usuarios = (programa?.usuarios || []).filter((u) => u && u !== '—');

  if (applied) {
    return (
      <div className="card animate-in text-center" style={{ padding: 'var(--space-12)' }}>
        <h3 style={{ marginBottom: 'var(--space-3)' }}>
          Gracias, te contactaremos apenas se seleccionen los elegidos
        </h3>
        <p className="text-sm" style={{ marginBottom: 'var(--space-6)' }}>
          Su postulación a {programa?.nombre || 'la convocatoria'} quedó radicada con el NIT {nit}.
        </p>
        <button className="btn btn-ghost btn-sm" onClick={onReset}>
          Volver al inicio
        </button>
      </div>
    );
  }

  return (
    <div className="card animate-in">
      <div className="flex items-center" style={{ gap: 'var(--space-2)' }}>
        <span className="badge badge-navy">Radicación virtual</span>
        {programa?.entidad && <span className="badge badge-outline">{programa.entidad}</span>}
        {programa?.id && (
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{programa.id}</span>
        )}
      </div>

      <h3 style={{ marginTop: 'var(--space-3)', marginBottom: 'var(--space-2)' }}>
        {programa?.nombre || 'Ruta Integral de Apoyo Empresarial – Convocatoria 2026'}
      </h3>
      <p className="text-sm">{programa?.descripcion || 'Convocatoria 2026 de apoyo empresarial.'}</p>

      <div className="divider" style={{ margin: 'var(--space-5) 0' }} />

      <Field
        label="Objetivo de política"
        value={objetivos.length ? objetivos.join(', ') : 'Calidad / Productividad y Competitividad'}
      />
      <Field label="Cupos disponibles" value={`${CUPOS_SIMULADOS} empresas`} />
      <Field
        label="Público objetivo"
        value={usuarios.length ? usuarios.join(', ') : 'Micro, pequeñas y medianas empresas'}
      />

      <div className="divider" style={{ margin: 'var(--space-5) 0' }} />

      <h4 style={{ marginBottom: 'var(--space-3)', fontSize: '1rem' }}>
        Datos precargados de la empresa
      </h4>
      <Field label="NIT" value={nit} />
      <Field label="Razón social" value={datos?.nombre || '—'} />
      <Field label="Empleados" value={datos?.empleados ?? '—'} />
      <Field label="Sector" value={datos?.sector || '—'} />
      <Field label="Departamento" value={datos?.departamento || '—'} />

      <button className="btn btn-primary btn-block mt-6" onClick={handleApply}>
        Aplicar ya
      </button>
    </div>
  );
}

function Field({ label, value }) {
  return (
    <div className="flex" style={{ gap: 'var(--space-4)', marginBottom: 'var(--space-2)' }}>
      <span className="text-sm" style={{ color: 'var(--text-muted)', minWidth: '180px', flexShrink: 0 }}>
        {label}
      </span>
      <span className="text-sm" style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
        {value}
      </span>
    </div>
  );
}

export default ApplyStep;

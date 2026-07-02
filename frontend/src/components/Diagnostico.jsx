import { useState } from 'react';

const QUESTIONS = [
  {
    id: 'operacion',
    pillar: 'Pilar 1',
    title: 'Operación',
    text: '¿Cómo lleva el control diario de las ventas, inventarios y procesos de su negocio?',
    options: [
      { id: 'A', text: 'Todo lo llevo en un cuaderno, en papel o de memoria (operación manual).' },
      { id: 'B', text: 'Uso herramientas básicas (Excel, WhatsApp), pero la información suele estar desordenada o aislada.' },
      { id: 'C', text: 'Uso software especializado (contabilidad, ventas) o herramientas de IA de forma puntual.' },
      { id: 'D', text: 'Tengo la operación totalmente automatizada e integrada (sistemas ERP o IA conectada al núcleo de procesos).' },
    ],
  },
  {
    id: 'financiamiento',
    pillar: 'Pilar 2',
    title: 'Financiamiento',
    text: '¿De dónde proviene la mayor parte del dinero con el que funciona o crece su negocio?',
    options: [
      { id: 'A', text: 'De ahorros personales, préstamos familiares o la plata del día a día.' },
      { id: 'B', text: 'Genera ventas constantes, pero depende de microcrédito básico o ingresos diarios.' },
      { id: 'C', text: 'Depende de créditos de bancos tradicionales; a veces hay cuellos de botella en flujo de caja.' },
      { id: 'D', text: 'Cuenta con inversión privada, fondos de capital de riesgo o líneas de banca corporativa.' },
    ],
  },
  {
    id: 'mercado',
    pillar: 'Pilar 3',
    title: 'Mercado',
    text: '¿Dónde está ubicada la mayoría de sus clientes actuales?',
    options: [
      { id: 'A', text: 'En el barrio, municipio o zona de influencia directa (alcance hiper-local).' },
      { id: 'B', text: 'Principalmente en la ciudad o departamento (alcance local/regional).' },
      { id: 'C', text: 'Vende en varias regiones de Colombia y busca nuevos mercados nacionales.' },
      { id: 'D', text: 'Ya exporta o el modelo de negocio nació para vender en el exterior.' },
    ],
  },
  {
    id: 'innovacion',
    pillar: 'Pilar 4',
    title: 'Innovación',
    text: '¿Qué hace que su producto o servicio sea diferente al de la competencia?',
    options: [
      { id: 'A', text: 'Vende productos tradicionales; la competencia es principalmente por precio o ubicación.' },
      { id: 'B', text: 'Ofrece buena calidad y servicio al cliente, pero no tiene procesos de innovación estructurados.' },
      { id: 'C', text: 'Ha invertido en mejorar procesos internos, certificaciones o maquinaria para mayor eficiencia.' },
      { id: 'D', text: 'Tiene tecnología propia, patentes o usa IA avanzada para nuevos productos o modelos predictivos.' },
    ],
  },
  {
    id: 'objetivo',
    pillar: 'Transversal',
    title: 'Objetivo inmediato',
    text: 'Si el Estado pudiera resolver un solo reto estructural de su negocio hoy, ¿cuál elegiría?',
    options: [
      { id: 'A', text: 'Ayuda para estructurar la idea, formalizar legalmente o sobrevivir.' },
      { id: 'B', text: 'Capacitación para ordenar la casa, mejorar ventas y separar finanzas.' },
      { id: 'C', text: 'Optimizar producción o acceder a crédito de capital de trabajo.' },
      { id: 'D', text: 'Apoyo especializado para exportar, internacionalizarse o levantar inversión de alto impacto.' },
    ],
  },
];

function Diagnostico({ apiUrl, userData, onComplete }) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [nlpText, setNlpText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSelect = (qId, optId) => {
    setAnswers((prev) => ({ ...prev, [qId]: optId }));
  };

  const handleNext = () => step < QUESTIONS.length && setStep((s) => s + 1);
  const handleBack = () => step > 0 && setStep((s) => s - 1);

  const handleSubmit = async () => {
    setLoading(true);
    const payload = { ...answers, necesidad_nlp: nlpText };

    try {
      const res = await fetch(`${apiUrl}/api/diagnostico`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identificador: userData.identificador, respuestas: payload }),
      });
      const data = await res.json();
      if (data.status === 'success') {
        onComplete({
          respuestas: payload,
          matches: data.matches,
          perfil_calculado: data.perfil_calculado,
          puntajes_radar: data.puntajes_radar,
          total_instrumentos: data.total_instrumentos_arco,
        });
      }
    } catch (err) {
      console.error('Error submitting diagnostico:', err);
    } finally {
      setLoading(false);
    }
  };

  const totalSteps = QUESTIONS.length + 1;
  const progress = ((step + 1) / totalSteps) * 100;

  return (
    <div className="animate-in" style={{ maxWidth: '720px', margin: '0 auto' }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 style={{ marginBottom: 'var(--space-1)' }}>Radar de Madurez Empresarial</h2>
          <p className="text-sm" style={{ marginBottom: 0 }}>
            {userData?.datos?.nombre || 'Emprendedor'} · Paso {step + 1} de {totalSteps}
          </p>
        </div>
        <span className="badge badge-navy">{step < QUESTIONS.length ? QUESTIONS[step].pillar : 'Final'}</span>
      </div>

      <div className="progress-container mb-8">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      {/* Question Card */}
      <div className="card card-elevated animate-in" key={step}>
        {step < QUESTIONS.length ? (
          <>
            <div className="mb-6">
              <span className="badge badge-gold mb-2">{QUESTIONS[step].title}</span>
              <h3 className="mt-3" style={{ fontSize: '1.1rem', lineHeight: '1.5' }}>
                {QUESTIONS[step].text}
              </h3>
            </div>

            <div className="flex-col gap-4 stagger" style={{ display: 'flex', gap: 'var(--space-3)' }}>
              {QUESTIONS[step].options.map((opt) => (
                <div
                  key={opt.id}
                  className={`card card-interactive animate-in ${
                    answers[QUESTIONS[step].id] === opt.id ? 'selected' : ''
                  }`}
                  onClick={() => handleSelect(QUESTIONS[step].id, opt.id)}
                  style={{ padding: 'var(--space-4) var(--space-5)' }}
                >
                  <div className="flex items-center" style={{ gap: 'var(--space-4)' }}>
                    <div style={{
                      width: '32px', height: '32px', borderRadius: 'var(--radius-sm)',
                      background: answers[QUESTIONS[step].id] === opt.id
                        ? 'var(--color-navy-800)' : 'var(--color-gray-100)',
                      color: answers[QUESTIONS[step].id] === opt.id
                        ? 'var(--text-inverse)' : 'var(--text-secondary)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontWeight: '700', fontSize: '0.8125rem', flexShrink: 0,
                      transition: 'all 0.15s ease',
                    }}>
                      {opt.id}
                    </div>
                    <span style={{ fontSize: '0.9375rem', lineHeight: '1.5' }}>{opt.text}</span>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          /* NLP free-text step */
          <>
            <div className="mb-6">
              <span className="badge badge-gold mb-2">Input NLP</span>
              <h3 className="mt-3" style={{ fontSize: '1.1rem', lineHeight: '1.5' }}>
                En sus propias palabras: ¿para qué necesita apoyo exactamente hoy?
              </h3>
              <p className="text-sm mt-2">
                Esta respuesta alimenta directamente al motor de emparejamiento semántico (NLP) para cruzar con la oferta ArCo.
              </p>
            </div>

            <div className="form-group">
              <textarea
                className="form-textarea"
                value={nlpText}
                onChange={(e) => setNlpText(e.target.value)}
                placeholder='Ej: "Necesito un crédito para comprar maquinaria", "Quiero exportar café a Europa", "Busco formalizar mi negocio"'
              />
            </div>
          </>
        )}

        {/* Navigation */}
        <div className="divider" />
        <div className="flex justify-between items-center">
          <button
            className="btn btn-outline btn-sm"
            onClick={handleBack}
            disabled={step === 0 || loading}
          >
            Anterior
          </button>

          {step < QUESTIONS.length ? (
            <button
              className="btn btn-primary"
              onClick={handleNext}
              disabled={!answers[QUESTIONS[step].id]}
            >
              Siguiente
            </button>
          ) : (
            <button
              className="btn btn-accent"
              onClick={handleSubmit}
              disabled={loading || !nlpText.trim()}
            >
              {loading ? 'Procesando emparejamiento…' : 'Finalizar y ver ofertas'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default Diagnostico;

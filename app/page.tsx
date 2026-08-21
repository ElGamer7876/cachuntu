import { SiteFooter, SiteHeader } from "./components";
import { InteractiveTerminal } from "./interactive-terminal";

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#contenido">Saltar al contenido</a>
      <SiteHeader />

      <main id="contenido">
        <section className="hero" id="inicio">
          <div className="hero-glow hero-glow-a" />
          <div className="hero-glow hero-glow-b" />
          <div className="shell hero-grid">
            <div>
              <p className="eyebrow"><span className="dot" /> Distribución Linux en desarrollo</p>
              <h1>Ubuntu, pero <span>más rápido, limpio</span> y listo desde el primer arranque.</h1>
              <p className="hero-lead">Cachuntu parte de Ubuntu para construir una experiencia cuidada, optimizada y sencilla de usar, sin dejar de ser útil para quienes quieren mirar bajo el capó.</p>
              <div className="hero-actions">
                <a className="button primary" href="#caracteristicas">Conocer Cachuntu</a>
                <a className="button secondary" href="#roadmap">Ver progreso</a>
                <a className="button secondary" href="#descargas">Descargas · sin ISO pública</a>
              </div>
              <div className="hero-meta" aria-label="Estado del proyecto">
                <span>Base Ubuntu</span><span>Proyecto abierto</span><span>En desarrollo activo</span>
              </div>
            </div>

            <InteractiveTerminal />
          </div>
        </section>

        <section className="strip" aria-label="Principios de Cachuntu">
          <div className="shell stat-grid"><div><strong>01</strong><span>Rendimiento real</span></div><div><strong>02</strong><span>Selección cuidadosa</span></div><div><strong>03</strong><span>Menos ajustes iniciales</span></div><div><strong>04</strong><span>Base familiar</span></div></div>
        </section>

        <section className="section" id="caracteristicas">
          <div className="shell">
            <div className="section-heading"><p className="eyebrow">Qué propone Cachuntu</p><h2>Una base conocida, afinada con intención.</h2><p>El proyecto prioriza decisiones útiles y transparentes. Nada de cifras inventadas: cada mejora deberá probarse antes de llegar a una versión pública.</p></div>
            <div className="feature-grid">
              {[
                ["Base Ubuntu", "Compatibilidad con el ecosistema de Ubuntu como punto de partida."],
                ["Rendimiento optimizado", "Ajustes medidos para lograr un sistema ágil desde el inicio."],
                ["Paquetes seleccionados", "Una selección útil, coherente y sin relleno innecesario."],
                ["Lista para usar", "Menos tareas repetitivas después de la instalación."],
                ["Personalización", "Una identidad propia que se mantiene práctica y familiar."],
                ["Herramientas técnicas", "Utilidades para usuarios que desean administrar y experimentar."],
                ["Escritorio cuidado", "Consistencia visual, accesibilidad y una experiencia limpia."],
              ].map(([title, text], index) => <article className="feature-card" key={title}><span className="feature-index">0{index + 1}</span><h3>{title}</h3><p>{text}</p></article>)}
            </div>
          </div>
        </section>

        <section className="section section-dark" id="ediciones">
          <div className="shell"><div className="section-heading"><p className="eyebrow">Ediciones</p><h2>Desktop primero. Lo demás, cuando esté listo.</h2></div><div className="edition-grid"><article className="edition-card featured"><span className="badge">EDICIÓN PRINCIPAL</span><h3>Cachuntu Desktop</h3><p>La experiencia principal prevista para equipos de escritorio y portátiles. Actualmente está en construcción.</p><ul><li>Base Ubuntu</li><li>Experiencia de escritorio cuidada</li><li>Configuración inicial optimizada</li></ul></article><article className="edition-card muted"><span className="badge quiet">IDEA FUTURA</span><h3>Cachuntu Minimal</h3><p>Una posible edición reducida o experimental. Su alcance y disponibilidad aún no están definidos.</p></article></div></div>
        </section>

        <section className="section" id="roadmap">
          <div className="shell roadmap-wrap"><div className="section-heading"><p className="eyebrow">Roadmap</p><h2>Del concepto a una ISO que podamos probar.</h2><p>El estado vive en una lista sencilla para poder actualizar cada fase sin rehacer la página.</p></div><ol className="roadmap"><li className="done"><span>1</span><div><strong>Concepto de Cachuntu</strong><small>Completado</small></div></li><li className="active"><span>2</span><div><strong>Identidad y presentación</strong><small>En progreso</small></div></li><li className="active"><span>3</span><div><strong>Construcción del sistema base</strong><small>En progreso</small></div></li><li><span>4</span><div><strong>Primera ISO booteable</strong><small>Próximo objetivo</small></div></li><li><span>5</span><div><strong>Pruebas en hardware y máquinas virtuales</strong><small>Pendiente</small></div></li><li><span>6</span><div><strong>Cachuntu Preview</strong><small>Pendiente</small></div></li><li><span>7</span><div><strong>Primera versión pública</strong><small>Pendiente</small></div></li></ol></div>
        </section>

        <section className="section download-section" id="descargas"><div className="shell"><div className="download-panel"><div><p className="eyebrow">Descargas</p><h2>La primera ISO de Cachuntu está en desarrollo.</h2><p>No publicaremos botones falsos ni datos inventados. Este espacio está preparado para versión, arquitectura, tamaño, ISO, SHA-256, notas, torrent y mirrors cuando existan.</p></div><div className="download-status"><span className="status-pill"><i /> En desarrollo</span><button className="button disabled" type="button" disabled>ISO aún no publicada</button><small>Próximo objetivo: primera ISO booteable</small></div></div></div></section>

        <section className="section faq-section" id="faq"><div className="shell two-col"><div className="section-heading"><p className="eyebrow">Preguntas frecuentes</p><h2>Qué es — y qué todavía no está decidido.</h2><p>Las respuestas separan lo confirmado de las decisiones que siguen abiertas.</p></div><div className="faq-list">
          <details><summary>¿Qué es Cachuntu?</summary><p>Una distribución Linux en desarrollo que parte de Ubuntu y busca una experiencia más limpia, afinada y lista para usar.</p></details>
          <details><summary>¿En qué distribución está basado?</summary><p>Cachuntu está basado en Ubuntu.</p></details>
          <details><summary>¿Es Ubuntu?</summary><p>No es una edición oficial de Ubuntu. Es un proyecto derivado con identidad, selección de paquetes y configuración propias.</p></details>
          <details><summary>¿Cachuntu utiliza paquetes de Ubuntu?</summary><p>La base prevista aprovecha el ecosistema de paquetes de Ubuntu. La selección concreta se definirá y documentará durante el desarrollo.</p></details>
          <details><summary>¿Cuándo estará disponible?</summary><p>No hay una fecha de lanzamiento anunciada. El próximo objetivo técnico es obtener una primera ISO booteable.</p></details>
          <details><summary>¿Será gratuito y open source?</summary><p>Sí. El código propio utiliza GPL-3.0-or-later y la documentación y recursos del proyecto usan CC BY-SA 4.0. El repositorio público ya está disponible.</p></details>
          <details><summary>¿Qué escritorio utilizará?</summary><p>Todavía no hay una decisión pública definitiva. Cuando se valide, se documentará aquí.</p></details>
          <details><summary>¿Podré instalar paquetes de Ubuntu?</summary><p>La compatibilidad con los paquetes de Ubuntu forma parte del objetivo de la base, pero deberá validarse antes de prometer detalles concretos.</p></details>
          <details><summary>¿Habrá una edición minimal?</summary><p>Cachuntu Minimal es una posibilidad futura o experimental; todavía no es un producto disponible ni tiene alcance definido.</p></details>
        </div></div></section>

        <section className="section section-dark" id="open-source"><div className="shell open-source"><div><p className="eyebrow">Open source</p><h2>Construido sobre tecnología abierta.</h2><p>Cachuntu crece como un proyecto abierto basado en Linux y otras tecnologías open source. El repositorio contiene por ahora la identidad, las licencias y la planificación inicial: todavía no existe una ISO ni una build instalable.</p></div><a className="repo-placeholder" href="https://github.com/ElGamer7876/cachuntu" rel="noreferrer" aria-label="Abrir el repositorio de Cachuntu en GitHub"><span>github</span><strong>ElGamer7876/cachuntu</strong><small>Ver código, licencias y progreso inicial →</small></a></div></section>
      </main>
      <SiteFooter />
    </>
  );
}

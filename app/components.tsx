import Link from "next/link";
import Image from "next/image";

const links = [
  ["Proyecto", "/about"],
  ["Descargas", "/download"],
  ["Roadmap", "/roadmap"],
  ["Documentación", "/docs"],
  ["Noticias", "/news"],
  ["Contribuir", "/contribute"],
];

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="shell nav-wrap">
        <Link className="brand" href="/" aria-label="Cachuntu, inicio">
          <Image src="/logo.svg" alt="" width={38} height={38} priority />
          <span>Cachuntu</span>
        </Link>
        <nav className="nav" aria-label="Navegación principal">
          <Link href="/#caracteristicas">Características</Link>
          <Link href="/roadmap">Roadmap</Link>
          <Link href="/docs">Documentación</Link>
          <Link className="nav-cta" href="/download">Descargas</Link>
        </nav>
        <details className="mobile-menu">
          <summary aria-label="Abrir navegación"><span /><span /><span /></summary>
          <nav aria-label="Navegación móvil">
            {links.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}
          </nav>
        </details>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="shell footer-grid">
        <div>
          <Link className="brand" href="/"><Image src="/logo.svg" alt="" width={34} height={34} /><span>Cachuntu</span></Link>
          <p>Una distribución basada en Ubuntu enfocada en rendimiento, limpieza y una experiencia lista para usar.</p>
        </div>
        <div><strong>Proyecto</strong>{links.slice(0, 3).map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}</div>
        <div><strong>Recursos</strong>{links.slice(3).map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}<a href="https://github.com/ElGamer7876/cachuntu" rel="noreferrer">GitHub</a></div>
        <div><strong>Legal</strong><Link href="/legal">Aviso legal</Link><span aria-disabled="true">Dirección pública · próximamente</span></div>
      </div>
      <div className="shell footer-bottom"><span>© Cachuntu.</span><span>Cachuntu no está afiliado, patrocinado ni aprobado por Canonical Ltd. Ubuntu es una marca registrada de Canonical Ltd.</span></div>
    </footer>
  );
}

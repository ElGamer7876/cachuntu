import Link from "next/link";
import { SiteFooter, SiteHeader } from "./components";

export type PageSection = { title: string; text: string; items?: string[] };

export function ContentPage({ eyebrow, title, intro, status, sections }: { eyebrow: string; title: string; intro: string; status?: string; sections: PageSection[] }) {
  return (
    <>
      <a className="skip-link" href="#contenido">Saltar al contenido</a>
      <SiteHeader />
      <main id="contenido" className="inner-main">
        <section className="inner-hero"><div className="shell"><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{intro}</p>{status && <span className="inner-status">{status}</span>}</div></section>
        <section className="inner-content"><div className="shell content-grid">
          {sections.map((section) => <article className="content-card" key={section.title}><h2>{section.title}</h2><p>{section.text}</p>{section.items && <ul>{section.items.map(item => <li key={item}>{item}</li>)}</ul>}</article>)}
        </div><div className="shell inner-back"><Link className="button secondary" href="/">← Volver al inicio</Link></div></section>
      </main>
      <SiteFooter />
    </>
  );
}

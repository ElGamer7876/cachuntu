import Link from "next/link";
import { SiteFooter, SiteHeader } from "./components";
export default function NotFound() { return <><SiteHeader /><main className="not-found"><div className="shell"><p className="error-code">404</p><h1>Esta ruta todavía no existe.</h1><p>Puede que el contenido siga en construcción o que el enlace sea incorrecto.</p><Link className="button primary" href="/">Volver al inicio</Link></div></main><SiteFooter /></>; }

"use client";

import Image from "next/image";
import { useRef } from "react";

export function InteractiveTerminal() {
  const cardRef = useRef<HTMLDivElement>(null);
  const frameRef = useRef<number | null>(null);

  const updateTilt = (clientX: number, clientY: number) => {
    const card = cardRef.current;
    if (!card || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    const bounds = card.getBoundingClientRect();
    const x = Math.min(1, Math.max(0, (clientX - bounds.left) / bounds.width));
    const y = Math.min(1, Math.max(0, (clientY - bounds.top) / bounds.height));
    card.style.setProperty("--terminal-rx", `${(0.5 - y) * 12}deg`);
    card.style.setProperty("--terminal-ry", `${(x - 0.5) * 14}deg`);
    card.style.setProperty("--terminal-mx", `${x * 100}%`);
    card.style.setProperty("--terminal-my", `${y * 100}%`);
  };

  return (
    <div
      ref={cardRef}
      className="terminal-card"
      aria-label="Vista conceptual del estado de Cachuntu"
      onPointerEnter={(event) => {
        if (event.pointerType === "touch") return;
        event.currentTarget.dataset.hovered = "true";
        updateTilt(event.clientX, event.clientY);
      }}
      onPointerMove={(event) => {
        if (event.pointerType === "touch") return;
        const { clientX, clientY } = event;
        if (frameRef.current !== null) cancelAnimationFrame(frameRef.current);
        frameRef.current = requestAnimationFrame(() => updateTilt(clientX, clientY));
      }}
      onPointerLeave={(event) => {
        delete event.currentTarget.dataset.hovered;
        event.currentTarget.style.removeProperty("--terminal-rx");
        event.currentTarget.style.removeProperty("--terminal-ry");
        event.currentTarget.style.removeProperty("--terminal-mx");
        event.currentTarget.style.removeProperty("--terminal-my");
        if (frameRef.current !== null) cancelAnimationFrame(frameRef.current);
        frameRef.current = null;
      }}
    >
      <span className="terminal-glare" aria-hidden="true" />
      <div className="terminal-top"><span className="traffic"><i /><i /><i /></span><span>cachuntu@dev:~</span></div>
      <div className="terminal-body">
        <p><span className="prompt">$</span> cachuntu status</p>
        <p className="terminal-output">Leyendo estado del proyecto...</p>
        <div className="terminal-logo"><Image src="/logo.svg" alt="" width={92} height={92} /><div><strong>Cachuntu</strong><span>ubuntu-based / work in progress</span></div></div>
        <dl className="terminal-stats"><div><dt>Base</dt><dd>Ubuntu</dd></div><div><dt>Edición</dt><dd>Desktop</dd></div><div><dt>ISO pública</dt><dd>No disponible</dd></div><div><dt>Objetivo</dt><dd>Primer arranque afinado</dd></div></dl>
      </div>
    </div>
  );
}

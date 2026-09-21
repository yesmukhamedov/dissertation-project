// src/components.js — Reusable UI components for DR Dashboard
import { useState } from 'react';
import { C } from './data';
import { useLang } from './i18n';

export function Card({ label, value, delta, color, sub }) {
  // A figure, not a tile: the colour lives in a short rule above the number,
  // so a row of five metrics reads as one measured line rather than a
  // patchwork of pastel boxes.
  const accent = C[color] || C.gray;
  return (
    <div className="metric-card" style={{
      flex: 1, minWidth: 110, padding: '10px 14px 12px',
      background: 'var(--color-background-primary)',
      border: '1px solid var(--color-border-tertiary)', borderRadius: 10,
      boxShadow: `inset 0 3px 0 ${accent}`,
    }}>
      <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', marginTop: 2 }}>{label}</div>
      <div style={{ fontSize: 21, fontWeight: 600, letterSpacing: '-0.01em', color: 'var(--color-text-primary)', marginTop: 3 }}>{value}</div>
      {delta && (
        <div style={{ fontSize: 11, fontWeight: 500, color: (delta.includes('✓') || delta.includes('+')) ? C.green : C.red, marginTop: 1 }}>
          {delta}
        </div>
      )}
      {sub && <div style={{ fontSize: 10.5, color: 'var(--color-text-tertiary)', marginTop: 2 }}>{sub}</div>}
    </div>
  );
}

export function Note({ children }) {
  return (
    <div style={{
      fontSize: 12, color: 'var(--color-text-secondary)',
      padding: '9px 14px', background: 'var(--color-background-secondary)',
      borderLeft: '2px solid var(--color-border-primary)',
      borderRadius: '0 8px 8px 0', marginTop: 10, lineHeight: 1.6,
    }}>
      {children}
    </div>
  );
}

export function Hbar({ items, maxV, height = 20 }) {
  const mx = maxV || Math.max(...items.map(i => i.v)) * 1.1;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      {items.map((it, i) => (
        <div key={i} className="hbar-row" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div className="hbar-label" style={{ fontSize: 11, color: 'var(--color-text-secondary)', minWidth: 150, textAlign: 'right', lineHeight: 1.25 }}>
            {it.label}
          </div>
          <div className="keep-row" style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ flex: 1, height, background: 'var(--color-background-secondary)', borderRadius: 3, overflow: 'hidden' }}>
              <div style={{ width: `${(it.v / mx) * 100}%`, height: '100%', background: it.color || C.blue, borderRadius: 3 }} />
            </div>
            <span style={{ width: 40, flexShrink: 0, fontSize: 11, fontWeight: 600, textAlign: 'right' }}>
              {it.v.toFixed ? it.v.toFixed(3) : it.v}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export function Paired({ items, c1 = C.gray, c2 = C.teal, l1 = 'Baseline', l2 = 'Pipeline' }) {
  const mx = Math.max(...items.flatMap(i => [i.a, i.b])) * 1.12;
  return (
    <div>
      <div style={{ display: 'flex', gap: 14, fontSize: 10, color: 'var(--color-text-secondary,#666)', marginBottom: 6 }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <span style={{ width: 8, height: 8, borderRadius: 2, background: c1, display: 'inline-block' }} />{l1}
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <span style={{ width: 8, height: 8, borderRadius: 2, background: c2, display: 'inline-block' }} />{l2}
        </span>
      </div>
      {items.map((it, i) => (
        <div key={i} style={{ marginBottom: 8 }}>
          <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#666)', marginBottom: 2 }}>{it.label}</div>
          {[{ v: it.a, c: c1 }, { v: it.b, c: c2 }].map((b, bi) => (
            <div key={bi} className="keep-row" style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 2 }}>
              <div style={{ flex: 1, height: 14, background: 'var(--color-background-secondary)', borderRadius: 3, overflow: 'hidden' }}>
                <div style={{ width: `${(b.v / mx) * 100}%`, height: '100%', background: b.c, borderRadius: 3 }} />
              </div>
              <span style={{ width: 40, flexShrink: 0, fontSize: 11, fontWeight: 600, textAlign: 'right' }}>
                {b.v.toFixed(3)}
              </span>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export function Sec({ title, note, step, children }) {
  return (
    <section className="sec">
      <h3 className="sec-title">
        {step != null && <span className="sec-step" aria-hidden="true">{step}</span>}
        <span>{title}</span>
      </h3>
      {children}
      {note && <Note>{note}</Note>}
    </section>
  );
}

export function DataTable({ headers, rows, highlightRow }) {
  return (
    <div className="table-scroll" style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11 }}>
        <thead>
          <tr style={{ borderBottom: '1.5px solid var(--color-text-primary)' }}>
            {headers.map((h, i) => (
              <th key={i} style={{ padding: '6px 8px', textAlign: i === 0 ? 'left' : 'center', fontWeight: 600, fontSize: 11, color: 'var(--color-text-secondary)' }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => {
            const hl = !!(highlightRow && highlightRow(row, i));
            return (
            <tr key={i} className={hl ? 'row-hl' : undefined} style={{
              borderBottom: '1px solid var(--color-border-tertiary,#eee)',
              background: hl ? C.amberBg : 'transparent',
            }}>
              {row.map((cell, j) => (
                <td key={j} style={{
                  padding: '6px 8px',
                  textAlign: j === 0 ? 'left' : 'center',
                  fontWeight: j === 0 ? 500 : 400,
                  color: typeof cell === 'string' && cell.includes('✓') ? C.teal : 'inherit',
                }}>
                  {cell}
                </td>
              ))}
            </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export function ImageFigure({ src, caption, figNum }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <img
        src={src}
        alt={caption || ''}
        style={{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)', display: 'block' }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4 }}>
          {figNum && <strong>Fig. {figNum}. </strong>}{caption}
        </div>
      )}
    </div>
  );
}

export function DiagramViewer({ src, alt, caption, tooltip }) {
  const [show, setShow] = useState(false);
  const { t } = useLang();
  const tooltipText = tooltip && tooltip.startsWith('tooltip.') ? t(tooltip) : tooltip;
  return (
    <div
      style={{ marginBottom: 16, position: 'relative' }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onClick={() => setShow(s => !s)}
    >
      <img
        src={src}
        alt={alt || caption || ''}
        style={{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)', display: 'block', background: '#fff', cursor: tooltipText ? 'help' : 'default' }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4, textAlign: 'center' }}>
          {caption}
        </div>
      )}
      {show && tooltipText && (
        <div className="tooltip-bubble" style={{
          position: 'absolute', bottom: '100%', left: '50%',
          transform: 'translateX(-50%)', marginBottom: 8,
          padding: '10px 14px', background: 'rgba(0,0,0,0.88)', color: 'white',
          borderRadius: 8, fontSize: 12, lineHeight: 1.5,
          maxWidth: 380, width: 'max-content', zIndex: 1000,
          pointerEvents: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        }}>
          {tooltipText}
          <div style={{
            position: 'absolute', top: '100%', left: '50%',
            transform: 'translateX(-50%)',
            width: 0, height: 0,
            borderLeft: '6px solid transparent', borderRight: '6px solid transparent',
            borderTop: '6px solid rgba(0,0,0,0.88)',
          }} />
        </div>
      )}
    </div>
  );
}

export function ImageWithTooltip({ src, alt, tooltip, figNum, caption, style }) {
  const [show, setShow] = useState(false);
  const { t } = useLang();
  const tooltipText = tooltip && tooltip.startsWith('tooltip.') ? t(tooltip) : tooltip;
  return (
    <div
      style={{ position: 'relative', marginBottom: 16, ...(style || {}) }}
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onClick={() => setShow(s => !s)}
    >
      <img
        src={src}
        alt={alt || caption || ''}
        style={{ width: '100%', borderRadius: 8, border: '1px solid var(--color-border-tertiary,#eee)', cursor: 'help', display: 'block' }}
      />
      {caption && (
        <div style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)', marginTop: 4, lineHeight: 1.4 }}>
          {figNum && <strong>Fig. {figNum}. </strong>}{caption}
        </div>
      )}
      {show && tooltipText && (
        <div className="tooltip-bubble" style={{
          position: 'absolute', bottom: '100%', left: '50%',
          transform: 'translateX(-50%)', marginBottom: 8,
          padding: '10px 14px', background: 'rgba(0,0,0,0.88)', color: 'white',
          borderRadius: 8, fontSize: 12, lineHeight: 1.5,
          maxWidth: 380, width: 'max-content', zIndex: 1000,
          pointerEvents: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        }}>
          {tooltipText}
          <div style={{
            position: 'absolute', top: '100%', left: '50%',
            transform: 'translateX(-50%)',
            width: 0, height: 0,
            borderLeft: '6px solid transparent', borderRight: '6px solid transparent',
            borderTop: '6px solid rgba(0,0,0,0.88)',
          }} />
        </div>
      )}
    </div>
  );
}

export function LangSwitcher() {
  const { lang, setLang } = useLang();
  const label = lang === 'en' ? 'EN' : 'ҚАЗ';
  const other = lang === 'en' ? 'ҚАЗ' : 'EN';
  const next = lang === 'en' ? 'kz' : 'en';
  return (
    <button
      type="button"
      className="chip-toggle"
      onClick={() => setLang(next)}
      title={`Switch to ${other}`}
      aria-label={`Language: ${label}. Switch to ${other}`}
    >
      <span>{label}</span>
      <span className="chip-key" aria-hidden="true">/ {other}</span>
    </button>
  );
}

export function ModeSwitcher({ mode, setMode }) {
  // Both names stay visible, current one in ink: invitations sent to the
  // reviewing ophthalmologists tell them to switch to "Full" by that word.
  const isLite = mode === 'lite';
  return (
    <button
      type="button"
      className="chip-toggle"
      onClick={() => setMode(isLite ? 'full' : 'lite')}
      title={isLite ? 'Full: every experiment and result of the study' : 'Lite: the live demo alone'}
      aria-label={`View: ${isLite ? 'Lite' : 'Full'}. Switch to ${isLite ? 'Full' : 'Lite'}`}
    >
      <span className={isLite ? undefined : 'chip-key'}>Lite</span>
      <span className={isLite ? 'chip-key' : undefined}>Full</span>
    </button>
  );
}

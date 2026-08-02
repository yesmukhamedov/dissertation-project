import { C, IQ, IQ_LEVELS } from '../data';
import { Sec, DataTable, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ValQuality() {
  const { t } = useLang();
  const colors = [C.coral, C.amber, C.teal];

  return (
    <div>
      <Sec
        title={t('quality.imageQuality')}
        note="Measured on the real float outputs of the pipeline (n = 100 images), baseline level L0 vs full pipeline L7. CNR +18%: better lesion/background contrast. Entropy +7%: richer local detail. SSIM is measured against the ORIGINAL frame, so its decrease to 0.865 means the pipeline moves the image further from the raw capture — that is the intended behaviour, not a regression."
      >
        {IQ.map((d, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
            <span style={{ fontSize: 11, fontWeight: 500, minWidth: 160 }}>{d.m}</span>
            <span style={{ fontSize: 10, color: C.gray, minWidth: 32, textAlign: 'right' }}>{d.b}</span>
            <span style={{ fontSize: 10, color: 'var(--color-text-secondary,#888)' }}>→</span>
            <span style={{ fontSize: 12, fontWeight: 600, color: C.teal, minWidth: 36 }}>{d.a}</span>
            <div style={{ flex: 1, height: 8, background: 'var(--color-background-secondary,#eee)', borderRadius: 4, overflow: 'hidden', position: 'relative' }}>
              <div style={{ position: 'absolute', width: `${Math.min((d.b / d.a) * 83, 100)}%`, height: '100%', background: C.gray, opacity: 0.3, borderRadius: 4 }} />
              <div style={{ width: '83%', height: '100%', background: colors[i], borderRadius: 4, opacity: 0.6 }} />
            </div>
            <span style={{ fontSize: 11, fontWeight: 600, color: C.coral, minWidth: 45 }}>{d.pct}</span>
          </div>
        ))}

        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/16_image_quality.png'}
          caption="Image quality metrics before (baseline L0) and after (full pipeline L7) preprocessing. Flat-field correction drives the CNR gain; CLAHE drives the entropy gain."
          figNum={16}
          tooltip="tooltip.fig16"
        />
      </Sec>

      <Sec title="Per-Level Image Quality vs Classification">
        <DataTable
          headers={['Ablation level', 'CNR', 'Entropy (bits)', 'SSIM (vs original)', 'Weighted F1']}
          rows={IQ_LEVELS.map(d => [
            d.level, d.cnr.toFixed(2), d.entropy.toFixed(3), d.ssim.toFixed(3), d.f1.toFixed(4),
          ])}
          highlightRow={(row, i) => i === IQ_LEVELS.length - 1}
        />
        <Note>
          The full pipeline improves both image quality and classification — but the two do <strong>not</strong>
          track each other level by level:
          <br />• CNR peaks at L4 (flat-field, 28.60) while F1 keeps climbing to L7;
          <br />• the geometric levels L1–L3 add +2.85pp F1 with CNR and entropy essentially unchanged;
          <br />• L6 (augmentation) adds +0.95pp F1 with all three IQ metrics identical to L5 — expected, since
          Stage 6 is train-only while quality is measured on the validation configuration.
          <br /><br />
          Conclusion for the thesis: IQ metrics capture the photometric part of the pipeline's mechanism but not the
          geometric canonization or the augmentation, and are therefore <em>not</em> a sufficient predictor of the
          classification gain. Within a single stage the picture differs — in the flat-field σ sweep CNR and F1 peak
          together at σ = 0.07 (see H-2). Note the CNR normalization differs between the two, so absolute values are
          not comparable across tables.
        </Note>
      </Sec>

      <Sec title="Metric Definitions">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {[
            { name: 'CNR (Contrast-to-Noise Ratio)', def: 'Mean intensity difference between lesion/vessel and background regions, normalized by background noise standard deviation. Measures detectability.' },
            { name: 'Image Entropy (bits)', def: 'Shannon entropy of the pixel intensity histogram. Higher entropy indicates richer local detail and fewer compression artifacts.' },
            { name: 'SSIM (vs original frame)', def: 'Structural similarity between the preprocessed image and the untouched original. It falls monotonically along the pipeline (1.000 → 0.865) because each stage moves the image further from the raw capture — this is a measure of how much the pipeline changes, not a quality score to maximize.' },
          ].map((m, i) => (
            <div key={i} style={{ display: 'flex', gap: 10, padding: '8px 12px', background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 6 }}>
              <div style={{ minWidth: 200, fontWeight: 600, fontSize: 11, color: colors[i] }}>{m.name}</div>
              <div style={{ fontSize: 11, color: 'var(--color-text-primary,#333)', lineHeight: 1.5 }}>{m.def}</div>
            </div>
          ))}
        </div>
      </Sec>
    </div>
  );
}

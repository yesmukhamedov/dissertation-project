import { C, DEV, DEVICE_SPREAD } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ExpH6() {
  const { t } = useLang();
  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-6: Device Robustness Hypothesis
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 6 — Cross-device evaluation on external camera systems
        </div>
      </div>

      <Sec title={t('exp.deviceShift')}>
        <Paired
          items={DEV.map(d => ({ label: d.c, a: d.fb, b: d.fp }))}
          c1={C.gray}
          c2={C.coral}
          l1="Baseline"
          l2="Pipeline"
        />
        <DataTable
          headers={['Camera / Dataset', 'n', 'Baseline F1', 'Pipeline F1', 'ΔF1', 'g (baseline)', 'g (pipeline)', '≥ 0.70']}
          rows={DEV.map(d => [
            d.c,
            d.n.toLocaleString(),
            d.fb.toFixed(4),
            d.fp.toFixed(4),
            `+${((d.fp - d.fb) * 100).toFixed(2)}pp`,
            d.gb ? d.gb.toFixed(4) : '1.0000',
            d.gp ? d.gp.toFixed(4) : '1.0000',
            d.gp ? (d.gp >= 0.70 ? '✓ / ✓' : '✗') : '—',
          ])}
          highlightRow={(row, i) => i === 0}
        />
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp6/10_exp6_device_shift.png'} caption="Cross-device F1 across the 5 external camera groups plus the in-domain reference. The pipeline (orange) beats the baseline (gray) everywhere, and by the widest margin on the most distant cameras: RFMiD (+9.70pp) and ODIR-5K (+8.80pp)." figNum={10} tooltip="tooltip.fig10" />
        <Note>
          Models trained exclusively on Canon CR-1 (EyePACS) and evaluated on 5 external camera groups without retraining.
          All 5 groups clear the g_floor = 0.70 for <strong>both</strong> arms (pipeline minimum: 0.7909 on RFMiD), so
          the threshold on its own does not separate them — the real result is the collapse of the spread below.
          <br /><br />
          The gain scales inversely with how well the group already worked: largest on RFMiD (+9.70pp, the baseline's
          worst group) and ODIR-5K (+8.80pp), smallest on Messidor-2 (+5.10pp, the baseline's best). The pipeline
          lifts the floor rather than raising the ceiling.
        </Note>
      </Sec>

      <Sec title={t('exp.variance')}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 12 }}>
          <Card label="std F1 (Baseline)" value="0.0281" color="red" sub="across 5 camera groups" />
          <Card label="std F1 (Pipeline)" value="0.0106" color="green" delta="2.6× narrower ✓" sub="CI [−0.0268, −0.0082]" />
          <Card label="std AUC (Baseline)" value="0.0210" color="red" sub="across 5 camera groups" />
          <Card label="std AUC (Pipeline)" value="0.0068" color="green" delta="3.1× narrower ✓" sub="CI [−0.0221, −0.0063]" />
        </div>
        <DataTable
          headers={['Spread measure', 'Baseline', 'Pipeline', 'Δ', '95% CI (Δ)', 'Factor']}
          rows={DEVICE_SPREAD.map(d => [
            d.metric,
            d.baseline.toFixed(4),
            d.pipeline.toFixed(4),
            d.delta.toFixed(4),
            `[${d.ci[0].toFixed(4)}, ${d.ci[1].toFixed(4)}]`,
            `${d.factor.toFixed(1)}×`,
          ])}
        />
        <Note>
          This is the substantive H-6 result. The between-device std of weighted F1 falls 2.6× and that of ROC-AUC
          3.1×; both CIs exclude zero. The g-ratio range narrows from 0.7310–0.8318 (span 0.101) to 0.7909–0.8275
          (span 0.037) — the pipeline makes model behaviour markedly more uniform across camera hardware.
          <br /><br />
          Computed across the 5 external camera groups (IDRiD, DDR, ODIR-5K, Messidor-2, RFMiD), excluding the
          EyePACS training domain. Evaluated from fold-0 checkpoints, so this std is <em>between-group</em>, not
          between-fold. In this run RFMiD is scored on the full 5-class scale (it was binary-only previously), so
          its numbers are not comparable with the earlier revision.
        </Note>
      </Sec>
    </div>
  );
}

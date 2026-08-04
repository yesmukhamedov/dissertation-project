import { C, CONFIGS, CLS, CLS_PR } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ResultsBestConfig() {
  const { t } = useLang();
  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          Config D — Best Single-Image Configuration
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Pipeline (4ch) + EfficientNet-B3 | EyePACS 100% (~35,126) | 5-fold CV
        </div>
      </div>

      <Sec title="Key Metrics">
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <Card label="Weighted F1" value={CONFIGS.D.f1.toFixed(4)} delta="+6.55pp vs Config C" color="blue" sub="EH-3 ≥ 5pp ✓" />
          <Card label="ROC-AUC" value={CONFIGS.D.auc.toFixed(4)} delta="+3.60pp vs Config C" color="teal" sub="EH-3 ≥ 2pp ✓" />
          <Card label="Cohen's κ" value={CONFIGS.D.k.toFixed(4)} delta="+11.03pp vs Config C" color="purple" sub="No degradation ✓" />
          <Card label="Accuracy" value={CONFIGS.D.acc.toFixed(4)} delta="+7.79pp vs Config C" color="amber" />
        </div>
        <Note>
          Config D achieves +6.55pp weighted F1 and +3.60pp AUC over the baseline (Config C, same architecture).
          Statistical significance: DeLong p=0.0028, McNemar p=0.0041, bootstrap 95% CI for ΔF1 [+4.23pp, +8.01pp],
          Holm-corrected p_adj=0.0056. macro-F1 rises further than weighted F1 (0.4300 → 0.5355, +10.55pp), i.e. the
          gain is concentrated on the minority grades.
        </Note>
      </Sec>

      <Sec title={t('results.perClassF1')}>
        <Paired
          items={CLS.map(d => ({ label: `${d.g} (n≈${d.n.toLocaleString()})`, a: d.b, b: d.pp }))}
          c1={C.gray}
          c2={C.teal}
          l1="Baseline (C)"
          l2="Pipeline (D)"
        />
        <DataTable
          headers={['DR Grade', 'N (samples)', 'Baseline F1', 'Pipeline F1', 'ΔF1', 'Relative']}
          rows={CLS.map(d => [
            d.g, d.n.toLocaleString(), d.b.toFixed(4), d.pp.toFixed(4),
            `+${((d.pp - d.b) * 100).toFixed(2)}pp`,
            `+${((d.pp - d.b) / d.b * 100).toFixed(0)}%`,
          ])}
          highlightRow={(row, i) => i === 1}
        />
        <Note>
          DR 1 (mild NPDR) is by far the hardest class — subtle microaneurysms plus severe imbalance (n = 2,443 of 35,126).
          The pipeline more than doubles its F1 (0.0976 → 0.2188, +124% relative), but the absolute level stays low
          (≈0.22): preprocessing mitigates the early-signs problem, it does not solve it.
          The largest absolute gains are DR 4 (+13.36pp) and DR 2 (+12.78pp). DR 0 is near-saturated at baseline
          (0.8889) and still gains +4.44pp.
        </Note>
      </Sec>

      <Sec title={t('results.perClassAUC')}>
        <DataTable
          headers={['DR Grade', 'Precision (C)', 'Recall (C)', 'Precision (D)', 'Recall (D)', 'ΔRecall']}
          rows={CLS_PR.map(d => [
            d.g, d.precB.toFixed(4), d.recB.toFixed(4), d.precP.toFixed(4), d.recP.toFixed(4),
            `+${((d.recP - d.recB) * 100).toFixed(2)}pp`,
          ])}
        />
        <Note>
          Per-class ROC-AUC was not recorded in this run — precision/recall are shown instead. Recall rises on every
          grade, and most on the minority ones (DR 3 +13.06pp, DR 1 +12.94pp, DR 4 +13.56pp), while precision rises
          too — so the gain is not a recall-for-precision trade.
        </Note>
      </Sec>

      <Sec title="Confusion Matrix">
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/exp1/20_confusion_matrix.png'}
          caption="Confusion matrix for Config D (n = 35,126). Strong diagonal dominance. Remaining confusions are adjacent on the severity scale — DR 0↔DR 1 (1,872 + 1,016 images) and DR 2↔DR 3. Distant errors are almost gone: DR 0→DR 4 falls from 23 images in Config C to 4 in Config D, which is what drives the +11.03pp gain in quadratic κ."
          figNum={20}
          tooltip="tooltip.fig20"
        />
      </Sec>
    </div>
  );
}

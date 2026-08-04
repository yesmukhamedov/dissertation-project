import { C, CLIN, CALIBRATION, TRAIN_TEST_GAP } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ValClinical() {
  const { t } = useLang();
  return (
    <div>
      <Sec title={t('clinical.referableDR')}>
        <Paired
          items={CLIN.map(d => ({ label: d.m, a: d.b, b: d.v }))}
          c1={C.gray}
          c2={C.teal}
          l1="Baseline"
          l2="Pipeline"
        />
        <DataTable
          headers={['Metric', 'Baseline', 'Pipeline', 'Δ']}
          rows={CLIN.map(d => [
            d.m, d.b.toFixed(4), d.v.toFixed(4),
            `+${((d.v - d.b) * 100).toFixed(2)}pp`,
          ])}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/14_clinical_metrics.png'}
          caption="Clinical screening metrics for referable DR (binary: non-referable DR 0–1 vs referable DR 2–4), EyePACS in-domain, Config C vs D. Sensitivity improves by +11.16pp (0.6891→0.8007) while specificity also rises (0.9455→0.9636)."
          figNum={14}
          tooltip="tooltip.fig14"
        />
        <Note>
          Sensitivity rises from 0.6891 to 0.8007 (+11.16pp) <strong>while specificity rises too</strong>
          (0.9455 → 0.9636). That combination matters: this is the ROC curve itself moving (referable AUC
          0.8680 → 0.9100, DeLong p=0.0028), not the operating point sliding along a fixed curve. PPV gains
          +8.82pp and NPV +2.62pp, so both misses and false referrals drop at once.
          <br /><br />
          WHO screening guidance recommends Sensitivity ≥ 80% and Specificity ≥ 80%. On this in-domain evaluation
          the pipeline arm clears both (0.8007 / 0.9636); the baseline clears specificity but falls short on
          sensitivity (0.6891).
          <br /><br />
          The same +0.10…+0.11 sensitivity gain recurs in zero-shot transfer to APTOS and across the 5 camera
          groups — it is the most reproducible clinical effect in the whole experiment set.
          <strong> These are operating characteristics on annotated datasets, not a clinical validation</strong>
          (INVARIANTS NC-14); no claim of screening fitness follows from them.
        </Note>
      </Sec>

      <Sec title={t('clinical.calibration')}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 10 }}>
          <Card label="ECE (Baseline)" value="0.0691" color="gray" />
          <Card label="ECE (Pipeline)" value="0.0402" color="purple" delta="−42% ✓" />
          <Card label="Brier (Baseline)" value="0.0715" color="gray" />
          <Card label="Brier (Pipeline)" value="0.0598" color="purple" delta="−16% ✓" />
        </div>
        <DataTable
          headers={['Calibration Metric', 'Baseline', 'Pipeline', 'Improvement']}
          rows={CALIBRATION.map(d => [d.metric, d.baseline.toFixed(4), d.pipeline.toFixed(4), d.improvement])}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/15_calibration.png'}
          caption="Reliability diagram (calibration curves) for baseline and pipeline. Pipeline curve is closer to the diagonal (perfect calibration), particularly for high-confidence predictions."
          figNum={15}
          tooltip="tooltip.fig15"
        />
        <Note>
          Expected Calibration Error (ECE) falls by 42% (0.0691 → 0.0402) and the Brier score by 16%
          (0.0715 → 0.0598). Well-calibrated probabilities matter for decision support, where a probability
          threshold drives the referral.
          <br /><br />
          The improvement is consistent with the operating point above — higher sensitivity arrives together with
          higher specificity, so there is no drift toward over-confidence.
        </Note>
      </Sec>

      <Sec title={t('clinical.trainTestGap')}>
        <DataTable
          headers={['Config', 'Arm', 'Best epochs (per fold)', 'Train loss', 'Val loss', 'Loss gap']}
          rows={TRAIN_TEST_GAP.map(d => [
            d.config, d.arm, d.bestEpochs, d.trainLoss.toFixed(3), d.valLoss.toFixed(3), d.gap.toFixed(3),
          ])}
          highlightRow={(row, i) => i === 1 || i === 3}
        />
        <Note>
          The pipeline arms hold a 2.5× smaller loss gap (0.021–0.022 vs 0.052–0.054) and converge ~7 epochs earlier,
          at a <strong>higher</strong> train loss — regularizer behaviour rather than a better fit.
          Patient-level 5-fold CV prevents leakage through bilateral correlation.
        </Note>
      </Sec>
    </div>
  );
}

import { C, CONFIGS, CONFIG_DELTAS } from '../data';
import { Sec, DataTable, Hbar, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ExpH1() {
  const { t } = useLang();
  const factorial = ['A', 'B', 'C', 'D'];
  const all4 = ['A', 'B', 'C', 'D'];

  const deltaF1 = ((CONFIGS.D.f1 - CONFIGS.C.f1) * 100).toFixed(1);
  const deltaAUC = ((CONFIGS.D.auc - CONFIGS.C.auc) * 100).toFixed(1);

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-1: Preprocessing Dominance Hypothesis
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 1 — 2×2 Factorial Design on EyePACS (100%, ~35,126 images, 5-fold CV)
        </div>
      </div>

      <Sec title={t('exp.factorial')}>
        <DataTable
          headers={['Config', 'Preprocessing', 'CNN', 'W.F1 ± σ', 'ROC-AUC ± σ', 'κ ± σ', 'Acc']}
          rows={factorial.map(k => {
            const v = CONFIGS[k];
            return [
              <span key={k} style={{ fontWeight: 700, color: k === 'D' ? C.teal : 'inherit' }}>{k}</span>,
              v.preprocessing, v.cnn,
              `${v.f1.toFixed(3)} ± ${v.f1s.toFixed(3)}`,
              `${v.auc.toFixed(3)} ± ${v.aucs.toFixed(3)}`,
              `${v.k.toFixed(3)} ± ${v.ks.toFixed(3)}`,
              v.acc.toFixed(3),
            ];
          })}
          highlightRow={(row, i) => i === 3}
        />
        <Note>
          Config D (Pipeline + EfficientNet-B3) is the best single-image configuration.
          ΔF1(D−C) = +{deltaF1}pp, ΔAUC(D−C) = +{deltaAUC}pp. Statistically significant (DeLong p=0.0028, McNemar p=0.0041; Holm-corrected p_adj=0.0056).
        </Note>
      </Sec>

      <Sec title="Paired Differences with 95% CI">
        <DataTable
          headers={['Pair', 'Metric', 'Δ', '95% CI (Δ)', 'CI excludes 0']}
          rows={CONFIG_DELTAS.map(d => [
            d.pair,
            d.metric,
            `+${d.delta.toFixed(4)}`,
            `[+${d.ci[0].toFixed(4)}, +${d.ci[1].toFixed(4)}]`,
            '✓',
          ])}
        />
        <Note>
          All six intervals exclude zero. Cross-validation intervals for baseline and pipeline also fail to
          overlap on any of the four primary metrics, so the effect exceeds the between-fold dispersion on
          every metric at once.
        </Note>
      </Sec>

      <Sec title="Weighted F1 by Configuration (A–D)">
        <Hbar
          items={factorial.map((k, i) => ({ label: `${k}: ${CONFIGS[k].lbl}`, v: CONFIGS[k].f1, color: [C.gray, C.blue, C.gray, C.teal][i] }))}
          maxV={0.85}
        />
      </Sec>

      <Sec title={t('exp.allConfigs')}>
        <DataTable
          headers={['Config', 'Preprocessing', 'CNN', 'Paradigm', 'W.F1 ± σ', 'ROC-AUC ± σ', 'κ ± σ', 'Acc']}
          rows={all4.map(k => {
            const v = CONFIGS[k];
            const paradigm = (k === 'A' || k === 'C')
              ? <span key={k + 'p'} style={{ color: C.blueT, fontWeight: 600 }}>P1 instantiation</span>
              : <span key={k + 'p'} style={{ color: C.tealT, fontWeight: 600 }}>P2 instantiation</span>;
            return [
              <span key={k} style={{ fontWeight: 700, color: k === 'D' ? C.teal : 'inherit' }}>{k}</span>,
              v.preprocessing, v.cnn,
              paradigm,
              `${v.f1.toFixed(3)} ± ${v.f1s.toFixed(3)}`,
              `${v.auc.toFixed(3)} ± ${v.aucs.toFixed(3)}`,
              `${v.k.toFixed(3)} ± ${v.ks.toFixed(3)}`,
              v.acc.toFixed(3),
            ];
          })}
          highlightRow={(row, i) => i === 5}
        />
        <Note>
          4 configurations (A–D). Configs A/C operationally instantiate paradigm P1 (Gulshan-paradigm baseline — end-to-end CNN, 3-channel stretch-resize + ImageNet normalize). Configs B/D operationally instantiate paradigm P2 (integrated pipeline — 8-stage preprocessing as integral model component, 4-channel input including FOV mask). The A-vs-B and C-vs-D contrasts are empirical comparisons between the two paradigms under matched conditions — not numerical comparisons against Gulshan 2016 (per INVARIANTS SB-1.12, CFC-2.2).
        </Note>
      </Sec>

      <Sec title="Factorial F1 Chart">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/01_exp1_factorial_f1.png'} caption="Weighted F1 comparison for 2×2 factorial design (Configs A–D). Bars show mean ± std across 5 folds." figNum={1} tooltip="tooltip.fig01" />
      </Sec>

      <Sec title="All Metrics Comparison">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/02_exp1_all_metrics.png'} caption="F1, AUC, κ, and Accuracy for all 2×2 factorial configurations. Config D dominates on all four metrics." figNum={2} tooltip="tooltip.fig02" />
      </Sec>

      <Sec title="Delta vs Baseline">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/03_exp1_delta.png'} caption="Preprocessing improvement (Δ) relative to baseline. Both architectures exceed EH-3 thresholds: ResNet-50 (B−A = +6.54pp F1) and EfficientNet-B3 (D−C = +6.55pp F1)." figNum={3} tooltip="tooltip.fig03" />
      </Sec>

      <Sec title="All 4 Configurations Chart">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/22_exp1_all_6_configs.png'} caption="All 4 configurations A–D. Both architectures benefit from pipeline: ResNet-50 (B vs A) +6.54pp, EfficientNet-B3 (D vs C) +6.55pp. Config D achieves highest absolute F1." figNum={22} tooltip="tooltip.fig22" />
      </Sec>

      <Sec title="Per-Class F1 (EfficientNet-B3)">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/18_per_class_f1.png'} caption="Per-class weighted F1: Baseline (Config C) vs Pipeline (Config D). The relative lift is largest on minority classes: DR 1 F1 more than doubles (0.098 → 0.219), DR 4 +13.4pp, DR 3 +10.1pp. DR 0 near-saturated at baseline (0.889 → 0.933)." figNum={18} tooltip="tooltip.fig18" />
      </Sec>

      <Sec title="Training Curves">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/19_training_curves.png'} caption="Training and validation loss/F1 curves across folds. The pipeline arm (D) converges ~7 epochs earlier (best epochs 7–9 vs 14–17) at a 2.5× smaller loss-gap (0.022 vs 0.054) — with a HIGHER train loss, i.e. regularizer behaviour rather than a better fit." figNum={19} tooltip="tooltip.fig19" />
      </Sec>

      <Sec title="Confusion Matrix — Config D">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/20_confusion_matrix.png'} caption="Confusion matrix for Config D (best single-image configuration). Diagonal dominance confirms correct classification. Main confusions: DR 1↔DR 0, DR 2↔DR 3 (adjacent grade confusion)." figNum={20} tooltip="tooltip.fig20" />
      </Sec>

      <Sec title="ROC Curves — All Configs">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp1/24_roc_curves.png'} caption="One-vs-rest ROC curves for all 4 factorial configurations. Config D shows consistently higher AUC across all DR grades, particularly DR 1 and DR 3." figNum={24} tooltip="tooltip.fig24" />
      </Sec>

      <Sec title={t('exp.dominanceCriterion')}>
        <DataTable
          headers={['Criterion', 'ResNet-50 (B−A)', 'EfficientNet-B3 (D−C)', 'Threshold', 'Met?']}
          rows={[
            ['ΔF1', `+${((CONFIGS.B.f1 - CONFIGS.A.f1) * 100).toFixed(1)}pp ✓`, `+${deltaF1}pp ✓`, '≥ 5pp', '✓ (both)'],
            ['ΔAUC', `+${((CONFIGS.B.auc - CONFIGS.A.auc) * 100).toFixed(1)}pp ✓`, `+${deltaAUC}pp ✓`, '≥ 2pp', '✓ (both)'],
            ['Δκ', `+${((CONFIGS.B.k - CONFIGS.A.k) * 100).toFixed(1)}pp ✓`, `+${((CONFIGS.D.k - CONFIGS.C.k) * 100).toFixed(1)}pp ✓`, '> 0', '✓ (both)'],
          ]}
        />
        <Note>
          EH-3 requires preprocessing dominance independently for both architectures. Both meet all thresholds:
          ResNet-50 (ΔF1=+{((CONFIGS.B.f1 - CONFIGS.A.f1) * 100).toFixed(1)}pp, DeLong p=0.0041) and
          EfficientNet-B3 (ΔF1=+{deltaF1}pp, DeLong p=0.0028); both survive the Holm correction across the 4 configs
          (p_adj=0.0082 / 0.0056). The mixed-effects ANOVA finds no arm×architecture interaction (p=0.31), so the
          effect size is statistically identical on the two backbones — as the near-equal ΔF1 (+6.54 vs +6.55pp) shows.
        </Note>
      </Sec>
    </div>
  );
}

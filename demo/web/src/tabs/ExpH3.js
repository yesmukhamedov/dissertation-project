import { C, APTOS, CONFIGS } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';

export default function ExpH3() {
  // Exp 3 was run on EfficientNet-B3 fold-0 checkpoints only — Configs A/B were not
  // evaluated on APTOS, so the comparison is C (baseline) vs D (pipeline).
  const configs = ['C', 'D'];

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-4: APTOS 2019 Cross-Dataset Transferability
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 3 — Zero-shot transfer of EyePACS-trained models to APTOS 2019 (n = 3,662; Indian population, mixed cameras)
        </div>
      </div>

      <Sec title="Generalization Ratio G — APTOS 2019">
        <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
          <Card
            label="G (Config C — Baseline EffNet-B3)"
            value={APTOS.C.G.toFixed(4)}
            delta={APTOS.C.G >= APTOS.threshold ? `≥ ${APTOS.threshold} ✓` : `< ${APTOS.threshold} ✗`}
            color={APTOS.C.G >= APTOS.threshold ? 'green' : 'red'}
            sub={`F1: ${APTOS.C.f1.toFixed(4)}`}
          />
          <Card
            label="G (Config D — Pipeline EffNet-B3)"
            value={APTOS.D.G.toFixed(4)}
            delta={APTOS.D.G >= APTOS.threshold ? `≥ ${APTOS.threshold} ✓` : `< ${APTOS.threshold} ✗`}
            color={APTOS.D.G >= APTOS.threshold ? 'green' : 'red'}
            sub={`F1: ${APTOS.D.f1.toFixed(4)}`}
          />
          <Card
            label="Δ weighted F1 (D − C)"
            value={`+${APTOS.deltaF1.toFixed(4)}`}
            delta={`95% CI [+${APTOS.deltaF1Ci[0].toFixed(4)}, +${APTOS.deltaF1Ci[1].toFixed(4)}]`}
            color="teal"
            sub="CI excludes zero"
          />
          <Card
            label="Δ ROC-AUC (D − C)"
            value={`+${APTOS.deltaAuc.toFixed(4)}`}
            delta={`95% CI [+${APTOS.deltaAucCi[0].toFixed(4)}, +${APTOS.deltaAucCi[1].toFixed(4)}]`}
            color="blue"
            sub="CI excludes zero"
          />
        </div>
        <Note>
          H-4 criterion: G = F1<sub>APTOS</sub> / F1<sub>EyePACS</sub> ≥ 0.85, and pipeline &gt; baseline.
          Both parts hold: G<sub>D</sub> = 0.8976 clears the threshold with 0.048 to spare, and the pipeline beats
          the baseline by +0.0889 weighted F1 (CI [+0.0681, +0.1197]).
          <strong> Important caveat:</strong> the baseline clears the threshold too (G<sub>C</sub> = 0.8577), so the
          "G ≥ 0.85" test on its own does not separate the two arms — the discriminating part of the hypothesis is
          "better than baseline". The honest phrasing is that the pipeline does not <em>rescue</em> transfer, it
          improves transfer that was already acceptable.
        </Note>
      </Sec>

      <Sec title="EyePACS (in-domain) vs APTOS 2019 (transfer) — F1">
        <Paired
          items={configs.map(k => ({
            label: `Config ${k}`,
            a: CONFIGS[k].f1,
            b: APTOS[k].f1,
          }))}
          c1={C.blue}
          c2={C.coral}
          l1="EyePACS (in-domain)"
          l2="APTOS 2019 (zero-shot)"
        />
        <DataTable
          headers={['Config', 'EyePACS F1', 'APTOS F1', 'APTOS AUC', 'APTOS κ', 'macro-F1', 'G', 'H-4']}
          rows={configs.map(k => [
            `${k} — ${CONFIGS[k].lbl}`,
            CONFIGS[k].f1.toFixed(4),
            APTOS[k].f1.toFixed(4),
            APTOS[k].auc.toFixed(4),
            APTOS[k].k.toFixed(4),
            APTOS[k].macroF1.toFixed(4),
            APTOS[k].G.toFixed(4),
            APTOS[k].G >= APTOS.threshold ? '✓' : '✗',
          ])}
          highlightRow={(_, i) => configs[i] === 'D'}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/exp3/29_exp3_aptos_transfer.png'}
          caption="APTOS 2019 zero-shot transfer. Both arms clear the H-4 threshold G ≥ 0.85; the pipeline (Config D, G = 0.8976) transfers measurably better than the baseline (Config C, G = 0.8577)."
          figNum={29}
        />
        <Note>
          G is normalized by each arm's <em>own</em> in-domain F1 (C: 0.7538, D: 0.8193). The stronger arm therefore
          carries a larger denominator, which makes ΔG (+0.040) a deliberately conservative view of an absolute
          APTOS gain of +0.089 — worth stating so the modest ΔG is not read as a weak effect.
        </Note>
      </Sec>

      <Sec title="Best-Config Detail (D) — Full APTOS Metrics">
        <DataTable
          headers={['Metric', 'Config C (baseline)', 'Config D (pipeline)', 'Δ']}
          rows={[
            ['F1 (weighted)', APTOS.C.f1.toFixed(4), APTOS.D.f1.toFixed(4), `+${(APTOS.D.f1 - APTOS.C.f1).toFixed(4)}`],
            ['ROC-AUC', APTOS.C.auc.toFixed(4), APTOS.D.auc.toFixed(4), `+${(APTOS.D.auc - APTOS.C.auc).toFixed(4)}`],
            ["Cohen's κ", APTOS.C.k.toFixed(4), APTOS.D.k.toFixed(4), `+${(APTOS.D.k - APTOS.C.k).toFixed(4)}`],
            ['Accuracy', APTOS.C.acc.toFixed(4), APTOS.D.acc.toFixed(4), `+${(APTOS.D.acc - APTOS.C.acc).toFixed(4)}`],
            ['macro-F1', APTOS.C.macroF1.toFixed(4), APTOS.D.macroF1.toFixed(4), `+${(APTOS.D.macroF1 - APTOS.C.macroF1).toFixed(4)}`],
            ['G (transfer ratio)', APTOS.C.G.toFixed(4), APTOS.D.G.toFixed(4), `+${(APTOS.D.G - APTOS.C.G).toFixed(4)}`],
          ]}
        />
        <Note>
          Training set: EyePACS (~35,126 images, Canon CR-1). Evaluation set: APTOS 2019 (3,662 images,
          mixed cameras, Indian population). Protocol: zero-shot — no retraining or fine-tuning on APTOS.
          The gain is present on <strong>all five</strong> DR grades, and macro-F1 rises more than weighted F1
          (+0.102 vs +0.089), i.e. the improvement is concentrated on the minority grades. κ gains most of all
          (+0.099): remaining errors stay adjacent on the severity scale.
          <br /><br />
          <strong>Caveat:</strong> evaluated from fold-0 checkpoints, so there is no between-fold variance for this
          experiment; the 95% CIs above are per-instance bootstrap intervals.
        </Note>
      </Sec>
    </div>
  );
}

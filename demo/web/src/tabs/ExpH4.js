import { C, GEN, GEN_AUC, G_RATIO, DEGRADATION, DOMAIN_DIST } from '../data';
import { Card, Sec, DataTable, Paired, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ExpH4() {
  const { t } = useLang();
  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          Cross-Dataset Transfer to External Clinical Sets
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 5 — Zero-shot generalization to IDRiD (n = 413) and Messidor-2 (n = 1,744); degradation criterion of H-7
        </div>
      </div>

      <Sec title={t('exp.genRatio')}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
          {G_RATIO.map(d => (
            <Card
              key={d.dataset}
              label={`G (${d.dataset})`}
              value={d.G_pipeline.toFixed(4)}
              delta={d.G_pipeline >= d.threshold ? `≥ ${d.threshold} ✓` : `< ${d.threshold} ✗`}
              color={d.G_pipeline >= d.threshold ? 'green' : 'red'}
              sub={`Baseline: ${d.G_baseline.toFixed(4)}`}
            />
          ))}
        </div>
        <Note>
          G = F1<sub>external</sub> / F1<sub>EyePACS</sub>, normalized by each arm's own in-domain F1
          (C: 0.7538, D: 0.8193). The G ≥ 0.85 threshold belongs to H-4 and applies to APTOS; for the clinical sets
          the applicable floor is the H-6 device floor of 0.70, which <strong>both</strong> arms clear on every dataset.
          <br /><br />
          Note the Messidor-2 row: G is marginally lower for the pipeline (0.8275 vs 0.8318) even though its absolute
          F1 is higher (0.6780 vs 0.6270). That is an artefact of the larger denominator, not a regression — the same
          normalization effect that makes Δ_drop unreliable below.
        </Note>
      </Sec>

      <Sec title={t('exp.crossDataset')}>
        <Paired
          items={GEN.map(d => ({ label: d.d, a: d.fb, b: d.fp }))}
          c2={C.blue}
          l1="Baseline"
          l2="Pipeline"
        />
        <DataTable
          headers={['Dataset', 'Baseline F1', 'Pipeline F1', 'ΔF1', 'G (baseline)', 'G (pipeline)']}
          rows={GEN.map(d => [
            d.d,
            d.fb.toFixed(4),
            d.fp.toFixed(4),
            `+${((d.fp - d.fb) * 100).toFixed(2)}pp`,
            d.Gb ? d.Gb.toFixed(4) : '1.0000',
            d.Gp ? d.Gp.toFixed(4) : '1.0000',
          ])}
        />
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp5/08_exp5_generalization.png'} caption="Cross-dataset F1 comparison: EyePACS (train), IDRiD (transfer), Messidor-2 (transfer). Pipeline reduces performance drop during domain shift." figNum={8} tooltip="tooltip.fig08" />
      </Sec>

      <Sec title="Cross-Dataset AUC">
        <DataTable
          headers={['Dataset', 'Baseline AUC', 'Pipeline AUC', 'ΔAUC']}
          rows={GEN_AUC.map(d => [
            d.dataset,
            d.baseline.toFixed(4),
            d.pipeline.toFixed(4),
            `+${((d.pipeline - d.baseline) * 100).toFixed(2)}pp`,
          ])}
        />
      </Sec>

      <Sec title="H-7: Clinical Degradation Criterion — Partially Confirmed">
        <DataTable
          headers={['Dataset', 'External F1 (C)', 'External F1 (D)', 'Δ F1', '95% CI (Δ)', 'p', 'Δ_drop (C)', 'Δ_drop (D)', 'Δ_full < Δ_base?']}
          rows={DEGRADATION.map(d => [
            d.dataset,
            d.extBaseline.toFixed(4),
            d.extPipeline.toFixed(4),
            `+${d.deltaF1.toFixed(4)}`,
            `[+${d.ci[0].toFixed(4)}, +${d.ci[1].toFixed(4)}]`,
            `${d.p.toFixed(4)} ✓`,
            `${d.delta_baseline.toFixed(2)}pp`,
            `${d.delta_pipeline.toFixed(2)}pp`,
            d.criterionMet ? '✓' : '✗',
          ])}
        />
        <Note>
          Two readings of H-7 give <strong>different answers</strong>, and both belong in the record.
          <br /><br />
          <strong>(a) As written</strong> — Δ_drop<sub>pipeline</sub> &lt; Δ_drop<sub>baseline</sub> — holds only on
          IDRiD, and by 0.45pp, which is an order of magnitude below the CI width. On Messidor-2 the sign reverses.
          Score: <strong>1 of 2 datasets</strong>. The claim "the pipeline is more resistant to clinical degradation"
          is not supported.
          <br /><br />
          <strong>(b) Absolute external performance</strong> is significantly higher on <strong>both</strong> sets
          (+0.0700, p = 0.0021 and +0.0510, p = 0.0138).
          <br /><br />
          The two disagree because Δ_drop is measured from each arm's own in-domain level, and the pipeline's is
          6.55pp higher — so the metric systematically penalizes the stronger arm. Relative degradation is in fact
          near-identical (16.8% vs 17.2% on Messidor-2). Defensible statement: the pipeline does not reduce the
          <em>proportional</em> drop under domain shift, but it is better at every point, external sets included.
        </Note>
      </Sec>

      <Sec title="H-3: Domain Distance — the Mechanism Behind Transfer">
        <DataTable
          headers={['Target domain', 'MMD (baseline)', 'MMD (pipeline)', 'Δd', '95% CI (Δd)', 'KL (baseline)', 'KL (pipeline)', 'KL reduction']}
          rows={DOMAIN_DIST.map(d => [
            d.domain,
            d.mmdBase.toFixed(4),
            d.mmdInt.toFixed(4),
            `+${d.dDelta.toFixed(4)}`,
            `[+${d.ci[0].toFixed(4)}, +${d.ci[1].toFixed(4)}]`,
            d.klBase.toFixed(4),
            d.klInt.toFixed(4),
            `−${((1 - d.klInt / d.klBase) * 100).toFixed(0)}%`,
          ])}
        />
        <Note>
          MMD over penultimate-layer features and KL over per-channel histograms. The distance to the source
          domain falls for <strong>all 6</strong> target domains on both measures, and every Δd interval excludes zero.
          <br /><br />
          Three points worth carrying into the text. (1) The KL reduction is nearly constant (−35…−37%) regardless
          of how far the domain started, so the pipeline compresses photometric spread by a fixed proportion rather
          than pulling distant domains up to near ones. (2) The <em>ordering</em> of domains is preserved — RFMiD
          stays furthest, Messidor-2 closest — so the residual difference between datasets is substantive
          (population, acquisition protocol) and preprocessing does not remove it. (3) Stage 7 normalizes with
          <strong> source-domain</strong> statistics, so the closing is achieved by stages 0–6 and is not a hidden
          form of target-domain adaptation.
          <br /><br />
          Domains with the largest Δd (RFMiD +0.0880, ODIR-5K +0.0850) are the ones with the largest F1 gain
          (+9.70pp, +8.80pp); the smallest Δd (Messidor-2 +0.0630) goes with the smallest gain (+5.10pp).
          <strong> This is an association over 6 points, not causation</strong> — no correlation test was run, and
          APTOS is an outlier on the gain side at an average Δd.
          <br /><br />
          <em>Caveat:</em> MMD is computed in each arm's own feature space, so what is compared is the relative
          remoteness of the target domain per model, not distances in one shared space.
        </Note>
      </Sec>

      <Sec title="Generalization Ratio G — Chart">
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp5/09_exp5_G_ratio.png'} caption="Generalization ratio G for IDRiD and Messidor-2, both arms. Both clear the 0.70 device floor on both datasets; the pipeline holds higher absolute F1 throughout." figNum={9} tooltip="tooltip.fig09" />
        <Note>
          Models trained on Canon CR-1 (EyePACS) evaluated on Kowa VX-10α (IDRiD) and Topcon TRC NW6 (Messidor-2)
          without any retraining. Evaluated from fold-0 checkpoints, so there is no between-fold variance here.
          These same two sets also appear in Experiment 6 as the camera groups <code>kowa_idrid</code> and
          <code>topcon_messidor2</code> — the numbers are identical.
        </Note>
      </Sec>
    </div>
  );
}

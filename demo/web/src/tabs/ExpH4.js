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
          Experiment 5 — Zero-shot generalization to IDRiD (n = 413) and Messidor-2 (n = 1,744); external clinical performance criterion of H-7
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
          Note the Messidor-2 row: G is marginally lower for the pipeline (0.8328 vs 0.8334) even though its absolute
          F1 is higher (0.6823 vs 0.6282). That is an artefact of the larger denominator, not a regression — the same
          normalization defect that retired the Δ_drop form of H-7 below.
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
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp5/08_exp5_generalization.png'} caption="Cross-dataset F1 comparison: EyePACS (train), APTOS 2019, IDRiD, Messidor-2. The pipeline holds higher absolute weighted F1 on every external set." figNum={8} tooltip="tooltip.fig08" />
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

      <Sec title="H-7: External Clinical Performance — Confirmed (2 of 2)">
        <DataTable
          headers={['Dataset', 'n', 'External F1 (C)', 'External F1 (D)', 'Δ F1', '95% CI (Δ)', 'p (1-sided)', 'Δ ≥ MCID 0.050', 'CI⁻ > 0', 'PASS_S']}
          rows={DEGRADATION.map(d => [
            d.dataset,
            d.n.toLocaleString(),
            d.extBaseline.toFixed(4),
            d.extPipeline.toFixed(4),
            `+${d.deltaF1.toFixed(4)}`,
            `[+${d.ci[0].toFixed(4)}, +${d.ci[1].toFixed(4)}]`,
            `${d.p.toFixed(4)} ✓`,
            `✓ (margin +${d.margin.toFixed(4)})`,
            `+${d.ci[0].toFixed(4)} ✓`,
            d.passS ? '1' : '0',
          ])}
        />
        <Note>
          The operative form of H-7 is <strong>external clinical performance</strong>: on each of the two external
          clinical sets the integrated arm must deliver Δ weighted F1 ≥ MCID = 0.050 with the lower CI bound above
          zero. Both sets pass, so Σ PASS = 2 = N and <strong>H-7 is confirmed</strong>. The sets are not aggregated —
          a single reversal on either would sink the hypothesis regardless of the other.
          <br /><br />
          <strong>Caveat that must be stated openly:</strong> on Messidor-2 the margin over the MCID is only 0.0041,
          and the lower CI bound (+0.0362) sits below the threshold. That is legitimate under the criterion — it
          requires Δ ≥ MCID <em>and</em> CI⁻ &gt; 0, not CI⁻ ≥ MCID — but the pass is real rather than comfortable,
          and a re-run that moves Δ by more than 0.0041 would flip that set.
        </Note>
      </Sec>

      <Sec title="Why Δ_drop was retired — a methodological result in its own right">
        <DataTable
          headers={['Dataset', 'Δ_drop (C)', 'Δ_drop (D)', 'Δ_drop(D) − Δ_drop(C)', 'Relative drop (C)', 'Relative drop (D)']}
          rows={DEGRADATION.map(d => [
            d.dataset,
            `${d.dropBase.toFixed(2)}pp`,
            `${d.dropPipe.toFixed(2)}pp`,
            `${(d.dropPipe - d.dropBase >= 0 ? '+' : '−')}${Math.abs(d.dropPipe - d.dropBase).toFixed(2)}pp`,
            `${d.relBase.toFixed(1)}%`,
            `${d.relPipe.toFixed(1)}%`,
          ])}
        />
        <Note>
          The earlier "degradation" form of H-7 — Δ_drop<sub>pipeline</sub> &lt; Δ_drop<sub>baseline</sub>, where
          Δ_drop = F1<sub>in-domain</sub> − F1<sub>external</sub> — is <strong>retired</strong>, and the reason is
          itself a contribution. The quantity is not independent of what it was meant to test:
          <br /><br />
          <code>Δ_drop(D) − Δ_drop(C) = Δ_in-domain − Δ_external = 0.0655 − Δ wF1(X)</code>
          <br /><br />
          Its sign is therefore fixed by a single question — does the external margin exceed the in-domain margin of
          6.55pp? — so the criterion demands that the pipeline beat the baseline <em>more on foreign data than on its
          own</em>, and penalizes it precisely for its in-domain win. It measures nothing about resistance. The
          identity checks out on both sets: IDRiD 0.0655 − 0.0689 = −0.0034; Messidor-2 0.0655 − 0.0541 = +0.0114.
          <br /><br />
          The relative figures corroborate it: once each arm is normalized by its own in-domain level the structural
          skew almost vanishes — 21.2% vs 19.1% on IDRiD, 16.7% vs 16.7% on Messidor-2. <strong>What must not be
          claimed is reduced degradation</strong>; what is claimed, and supported, is higher absolute external
          performance. The same defect recurs in the H-6 g_ratio, so one argument covers both metrics.
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
          Three points worth carrying into the text. (1) The KL reduction is nearly constant (−34…−38%) regardless
          of how far the domain started, so the pipeline compresses photometric spread by a fixed proportion rather
          than pulling distant domains up to near ones. (2) The <em>ordering</em> of domains is preserved — RFMiD
          stays furthest, Messidor-2 closest — so the residual difference between datasets is substantive
          (population, acquisition protocol) and preprocessing does not remove it. (3) Stage 7 normalizes with
          <strong> source-domain</strong> statistics, so the closing is achieved by stages 0–6 and is not a hidden
          form of target-domain adaptation.
          <br /><br />
          <strong>Report the direction only, not the magnitude.</strong> Only the extreme matches: RFMiD has both the
          largest distance reduction (+0.0931) and the largest F1 gain (+9.87pp). Below that the two orderings
          diverge — IDRiD is 2nd on Δd but 4th on gain, DDR sits at a middling Δd with the <em>smallest</em> gain of
          the six, and APTOS is 5th on Δd with the 2nd-largest gain (Spearman ρ ≈ 0.49 over 6 points). The mechanism
          is qualitatively consistent — distance falls everywhere, quality rises everywhere — but the size of the
          distance reduction does <strong>not</strong> predict the size of the gain.
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

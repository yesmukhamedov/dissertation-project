import { C, ABL, STAGE_CONTRIB, CLAHE1, CLAHE2, CLAHE_CLIP, CLAHE_THRESH, CLAHE_HELDOUT, FF_SWEEP, FF_HELDOUT } from '../data';
import { Sec, DataTable, Hbar, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ExpH2() {
  const { t } = useLang();
  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-2: Component Ablation + CLAHE/σ Sensitivity
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 2 — 8-level cumulative ablation + two-dimensional CLAHE sweep + flat-field σ sweep, all on EyePACS (100%, 5 folds, EfficientNet-B3)
        </div>
      </div>

      <Sec title={t('exp.ablation')}>
        <Hbar
          items={ABL.map((d, i) => ({ label: d.n, v: d.f1, color: i === 0 ? C.gray : i === ABL.length - 1 ? C.teal : C.blue }))}
          maxV={0.82}
        />
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp2/04_exp2_ablation.png'} caption="Cumulative ablation on full EyePACS (5 folds, single initialization across all levels): each row adds one pipeline stage. From baseline F1=0.7538 (numerically = Config C) to F1=0.8193 (= Config D) — +6.55pp, monotone in every individual fold." figNum={4} tooltip="tooltip.fig04" />
        <DataTable
          headers={['Pipeline State', 'F1', 'AUC', 'κ', 'ΔF1 vs Prev']}
          rows={ABL.map((d, i) => [
            d.n,
            d.f1.toFixed(4),
            d.auc.toFixed(4),
            d.k.toFixed(4),
            i === 0 ? '—' : `+${((d.f1 - ABL[i - 1].f1) * 100).toFixed(2)}pp`,
          ])}
          highlightRow={(row, i) => i === ABL.length - 1}
        />
        <Note>
          Every stage contributes significantly, and the contributions are near-uniform (+0.90…+1.00pp each).
          The whole spread of Δ across stages (0.10pp) is smaller than the between-fold σ (≈0.28pp), so the stages
          <strong> cannot be ranked against one another</strong> — there is no "leading stage". The pipeline behaves as an
          ensemble of comparably-strong normalizations whose effects add up.
          Because all 8 levels share a single initialization, the +6.55pp total is attributable to preprocessing
          alone — this is what decomposes the preprocessing × SSL-init confound (CFC-2.8) in Exp 1.
        </Note>
      </Sec>

      <Sec title={t('exp.perStage')}>
        <Hbar
          items={STAGE_CONTRIB.map(d => ({
            label: d.stage,
            v: d.delta_f1,
            color: d.significant ? C.teal : C.gray,
          }))}
          maxV={1.4}
        />
        <DataTable
          headers={['Stage', 'Marginal ΔF1 (pp)', '2·σ_fold band (pp)', 'Exceeds noise?']}
          rows={STAGE_CONTRIB.map(d => [
            d.stage,
            `+${d.delta_f1.toFixed(2)}pp`,
            `${d.band.toFixed(2)}pp`,
            d.significant ? '✓' : '✗',
          ])}
        />
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp2/05_exp2_per_stage.png'} caption="Marginal F1 contribution of each pipeline stage against the 2·σ_fold significance band. All 7 transitions clear the band, but the contributions are statistically indistinguishable from one another." figNum={5} tooltip="tooltip.fig05" />
        <Note>
          Δ is the contribution of stage j <em>given</em> stages 0…j−1 already applied — the ordering is fixed by the
          pipeline, so these are not isolated single-stage effects and inter-stage interactions are not measured here.
          Caveat: Stage 3 (FOV mask) is not isolated — level L3 adds Stages 2 and 3 together, because disabling the
          mask would require a 3-channel variant of the model.
        </Note>
      </Sec>

      <Sec title="H-2: CLAHE Parameter Sensitivity Heatmap">
        <Note>
          Dual-constraint CLAHE swept on <strong>EyePACS</strong> over the joint grid clip_factor ∈ [0.5–4.0] ×
          global_threshold ∈ [0.01–0.05] (8 × 5 = 40 points, train folds).
          Overall optimum θ* = (clip_factor 2.5, threshold 0.03), p_apply = 0.80.
          Per-class optima differ: DR 1 at (2.5, 0.03), DR 2 at (2.0, 0.03) — the finer lesions of DR 1 need a more
          aggressive clip. Both optima are <em>interior</em> to the tested range, which is what H-2 asserts.
          Over-enhancement (clip_factor &gt; 3.0) degrades performance by amplifying noise. ★ marks optimal cell.
        </Note>
        <DataTable
          headers={['Arm', 'Weighted F1', 'F1 (DR 1)', 'F1 (DR 2)']}
          rows={[
            ['CLAHE = off', CLAHE_HELDOUT.off.toFixed(4), CLAHE_HELDOUT.dr1Off.toFixed(4), CLAHE_HELDOUT.dr2Off.toFixed(4)],
            ['CLAHE = θ* (2.5, 0.03)', CLAHE_HELDOUT.optimal.toFixed(4), CLAHE_HELDOUT.dr1Opt.toFixed(4), CLAHE_HELDOUT.dr2Opt.toFixed(4)],
            ['Δ (held-out)', `+${CLAHE_HELDOUT.delta.toFixed(4)} · 95% CI [+${CLAHE_HELDOUT.ci[0].toFixed(4)}, +${CLAHE_HELDOUT.ci[1].toFixed(4)}]`, `+${(CLAHE_HELDOUT.dr1Opt - CLAHE_HELDOUT.dr1Off).toFixed(4)}`, `+${(CLAHE_HELDOUT.dr2Opt - CLAHE_HELDOUT.dr2Off).toFixed(4)}`],
          ]}
          highlightRow={(row, i) => i === 1}
        />
        {[['DR Grade 1 — F1', CLAHE1, C.coral], ['DR Grade 2 — F1', CLAHE2, C.teal]].map(([title, data, hi], ti) => {
          const flat = data.flat(), mx = Math.max(...flat);
          const mn = Math.min(...flat);
          return (
            <div key={ti} style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 12, fontWeight: 500, marginBottom: 4 }}>{title}</div>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ borderCollapse: 'collapse', fontSize: 10 }}>
                  <thead>
                    <tr>
                      <td style={{ padding: 3, fontSize: 9, color: 'var(--color-text-secondary,#888)' }}>clip↓ / thresh→</td>
                      {CLAHE_THRESH.map(g => (
                        <th key={g} style={{ padding: '3px 8px', fontWeight: 400, color: 'var(--color-text-secondary,#888)' }}>{g}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.map((row, ri) => (
                      <tr key={ri}>
                        <td style={{ padding: '3px 8px', fontWeight: 400, color: 'var(--color-text-secondary,#888)', textAlign: 'right' }}>
                          {CLAHE_CLIP[ri].toFixed(1)}
                        </td>
                        {row.map((v, ci) => {
                          const t = (v - mn) / (mx - mn);
                          const isMax = v === mx;
                          return (
                            <td key={ci} style={{
                              padding: '4px 8px', textAlign: 'center', fontWeight: isMax ? 700 : 400,
                              background: `rgba(${hi === C.coral ? '216,90,48' : '29,158,117'},${0.08 + t * 0.55})`,
                              color: t > 0.55 ? 'white' : 'inherit', borderRadius: 2,
                            }}>
                              {v.toFixed(2)}{isMax ? ' ★' : ''}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          );
        })}
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp2/13_exp2_clahe_sensitivity.png'} caption="CLAHE parameter sensitivity heatmap for DR grades 1 and 2. Optimal parameters identified at clip_factor=2.5 (DR 1) and 2.0 (DR 2) with global_threshold=0.03." figNum={13} tooltip="tooltip.fig13" />
        <Note>
          The grids are train-fold values used to <em>select</em> θ*, not a performance estimate. On held-out data the
          per-class figures diverge from the grid in both directions — F1(DR 1) is markedly lower (0.2088 vs 0.4700 at θ*),
          F1(DR 2) higher (0.6482 vs 0.6000). The held-out numbers are the ones to quote.
        </Note>
      </Sec>

      <Sec title="H-2: Flat-Field σ Sweep">
        <Hbar
          items={FF_SWEEP.map(d => ({
            label: `σ = ${d.sigma.toFixed(2)}·D`,
            v: d.f1,
            color: d.sigma === FF_HELDOUT.sigmaStar ? C.teal : C.blue,
          }))}
          maxV={0.85}
        />
        <DataTable
          headers={['σ / D_FOV', 'Weighted F1', 'CNR']}
          rows={FF_SWEEP.map(d => [d.sigma.toFixed(2), d.f1.toFixed(4), d.cnr.toFixed(2)])}
          highlightRow={(row, i) => FF_SWEEP[i].sigma === FF_HELDOUT.sigmaStar}
        />
        <DataTable
          headers={['Arm', 'Weighted F1']}
          rows={[
            ['flat-field = off', FF_HELDOUT.off.toFixed(4)],
            ['flat-field = σ* (0.07·D)', FF_HELDOUT.optimal.toFixed(4)],
            ['Δ (held-out)', `+${FF_HELDOUT.delta.toFixed(4)} · 95% CI [+${FF_HELDOUT.ci[0].toFixed(4)}, +${FF_HELDOUT.ci[1].toFixed(4)}]`],
          ]}
          highlightRow={(row, i) => i === 1}
        />
        <Note>
          Strictly unimodal with an interior maximum at σ* = 0.07·D and a symmetric fall-off on both sides.
          The range over the sweep (R = 0.052) is comparable to the entire pipeline effect, so σ is a parameter that
          genuinely has to be tuned rather than picked arbitrarily. σ* coincides with the value already fixed in the
          Stage 4 specification — the sweep confirms the existing setting rather than changing it.
          Within this one stage CNR and F1 move together (both peak at σ = 0.07); <em>across</em> stages they do not
          (see Validation → Image Quality). Note the CNR normalization here differs from the per-level table — the two
          are not comparable in absolute terms.
        </Note>
      </Sec>
    </div>
  );
}

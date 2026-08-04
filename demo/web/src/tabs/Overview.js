import { C, CONFIGS, HYPOTHESES, EXTRA_RESULTS } from '../data';
import { Card, Sec, DataTable, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function Overview() {
  const { t } = useLang();
  const D = CONFIGS.D;
  const deltaF1 = ((D.f1 - CONFIGS.C.f1) * 100).toFixed(1);
  const deltaAUC = ((D.auc - CONFIGS.C.auc) * 100).toFixed(1);

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, color: 'var(--color-text-primary,#222)', margin: '0 0 4px 0' }}>
          Automated Diabetic Retinopathy Diagnosis
        </h2>
        <p style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)', margin: '0 0 4px 0' }}>
          Fundus Image Enhancement and CNN Classification — PhD Dissertation
        </p>
        <div style={{ fontFamily: 'monospace', fontSize: 13, fontWeight: 600, color: C.teal, background: C.tealBg, display: 'inline-block', padding: '4px 10px', borderRadius: 6 }}>
          model = preprocessing + CNN
        </div>
      </div>

      <Sec title={t('overview.bestConfig')}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 10 }}>
          <Card label="Weighted F1" value={D.f1.toFixed(4)} delta={`+${deltaF1}pp vs Config C`} color="blue" sub="EH-3: ≥5pp ✓" />
          <Card label="ROC-AUC" value={D.auc.toFixed(4)} delta={`+${deltaAUC}pp vs Config C`} color="teal" sub="EH-3: ≥2pp ✓" />
          <Card label="Cohen's κ" value={D.k.toFixed(4)} delta={`+${((D.k - CONFIGS.C.k) * 100).toFixed(2)}pp vs Config C`} color="purple" sub="No degradation ✓" />
          <Card label="Accuracy" value={D.acc.toFixed(4)} delta={`+${((D.acc - CONFIGS.C.acc) * 100).toFixed(2)}pp vs Config C`} color="amber" />
        </div>
      </Sec>

      <Sec title="Summary Radar Chart">
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/11_summary_radar.png'}
          caption="Summary performance radar over six evaluation axes: in-domain weighted F1, ROC-AUC and κ, APTOS transfer ratio G, mean ALO, and the minimum device g_ratio. The pipeline polygon encloses the baseline on every axis."
          figNum={11}
          tooltip="tooltip.fig11"
        />
      </Sec>

      <Sec title={t('overview.hypothesisStatus')}>
        <DataTable
          headers={['Hypothesis', 'Name', 'Experiment', 'Status', 'Key Finding']}
          rows={[...HYPOTHESES, ...EXTRA_RESULTS].map(h => [
            <span key={h.id} style={{ fontWeight: 700, color: C.purple }}>{h.id}</span>,
            h.name,
            h.exp,
            <span key={h.id + 's'} style={{ color: h.status.startsWith('◐') ? C.amberT : C.teal, fontWeight: 600 }}>{h.status}</span>,
            h.detail,
          ])}
        />
        <div style={{ fontSize: 11, color: 'var(--color-text-secondary,#666)', lineHeight: 1.6, marginTop: 8 }}>
          All 7 hypotheses are confirmed; none are refuted. E-7 and A-1 sit outside the formal H-1…H-7 set.
        </div>
      </Sec>

      <Sec title="Object & Subject of Research">
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 240, padding: '10px 14px', background: C.blueBg, borderLeft: `3px solid ${C.blue}`, borderRadius: 6 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: C.blueT, letterSpacing: '0.04em', textTransform: 'uppercase', marginBottom: 4 }}>Object</div>
            <div style={{ fontSize: 11, color: C.blueT, lineHeight: 1.6 }}>
              Digital fundus images covering the five stages of diabetic retinopathy (DR 0–4) and the automated diagnostic process built upon them.
            </div>
          </div>
          <div style={{ flex: 1, minWidth: 240, padding: '10px 14px', background: C.tealBg, borderLeft: `3px solid ${C.teal}`, borderRadius: 6 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, letterSpacing: '0.04em', textTransform: 'uppercase', marginBottom: 4 }}>Subject</div>
            <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>
              The effect of integrating the preprocessing pipeline and CNN classifier into a single model on diagnostic effectiveness, generalization ability, and clinical explainability.
            </div>
          </div>
        </div>
      </Sec>

      <Sec title="Paradigmatic Context (P1 → P2)" note="The principal conceptual contribution of this dissertation is a paradigm shift from end-to-end CNN (P1) to integrated preprocessing-CNN (P2). Gulshan et al. (2016, JAMA) is taken as the canonical representative of P1 on the basis of its observable methodological practice (preprocessing deferred to supplement; main-text emphasis on architecture and data scale) — not on the basis of any explicit theoretical claim about preprocessing (per INVARIANTS SIR-9 / CFC-2.9). No direct numerical comparison with Gulshan is performed (per SB-1.12); differences in task, backbone, dataset partition, and validation protocol preclude a sound head-to-head test.">
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 240, padding: '10px 14px', background: C.blueBg, borderLeft: `3px solid ${C.blue}`, borderRadius: 6 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: C.blueT, letterSpacing: '0.04em', textTransform: 'uppercase', marginBottom: 4 }}>Paradigm P1 — end-to-end CNN</div>
            <div style={{ fontSize: 11, color: C.blueT, lineHeight: 1.6 }}>
              Preprocessing as ancillary data preparation. Canonical representative: <strong>Gulshan et al. (2016)</strong>. Followers: Pratt 2016, Rakhlin 2017, Saxena 2020, Ting 2017, Voets 2019. Operational instantiation in this dissertation: <strong>configs A/C</strong> in Experiment 1 (3-channel, stretch-resize + ImageNet normalize).
            </div>
          </div>
          <div style={{ flex: 1, minWidth: 240, padding: '10px 14px', background: C.tealBg, borderLeft: `3px solid ${C.teal}`, borderRadius: 6 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: C.tealT, letterSpacing: '0.04em', textTransform: 'uppercase', marginBottom: 4 }}>Paradigm P2 — model = preprocessing + CNN</div>
            <div style={{ fontSize: 11, color: C.tealT, lineHeight: 1.6 }}>
              Preprocessing as integral model component. Operational instantiation: <strong>configs B/D</strong> in Experiment 1 (4-channel, full 8-stage pipeline). The 8 stages are the engineering realisation of the P2 paradigm; the controlled factorial of Experiment 1 is its empirical test.
            </div>
          </div>
        </div>
      </Sec>

      <Sec
        title="Central Thesis"
        note="The 8-stage preprocessing pipeline (canonical orientation, FOV normalization, flat-field correction, dual-constraint CLAHE, augmentation) is an integral part of the diagnostic model — not ancillary data preparation. Preprocessing is the primary driver of classification improvement for 5-class DR grading. The pipeline preserves diagnostic features while normalizing cross-device variability."
      >
        <div style={{ padding: '12px 14px', background: C.tealBg, borderRadius: 8, fontSize: 12, color: C.tealT, lineHeight: 1.7 }}>
          <strong>Finding:</strong> Preprocessing produces a statistically significant improvement on both architectures:
          EfficientNet-B3 (+6.55pp F1, DeLong p=0.0028) and ResNet-50 (+6.54pp F1, DeLong p=0.0041); both survive the
          Holm correction across the 4 configs (p_adj = 0.0056 / 0.0082). The mixed-effects ANOVA finds no
          arm×architecture interaction (p=0.31), so the effect size is statistically the same on either backbone.
          The gain is decomposable: an 8-level cumulative ablation under a <em>single</em> initialization reproduces
          the whole +6.55pp, which separates the preprocessing contribution from the SSL-init contribution, and it
          localizes the mechanism — the two photometric stages (flat-field, CLAHE) carry 41% of the gain.
          Between-device F1 spread narrows 2.4×, transfer to APTOS reaches G = 0.8976 (threshold 0.85), and Grad-CAM
          attention aligns significantly better with annotated lesions on all 4 lesion types.
          <br /><br />
          <strong>Where the evidence stops:</strong> H-7 claims higher absolute performance on the external clinical
          sets, <em>not</em> reduced degradation — proportionally the two arms drop almost equally (21.2%/19.1% on
          IDRiD, 16.7%/16.7% on Messidor-2), and the Messidor-2 margin over the MCID is only 0.0041. The H-4 and H-6
          thresholds are cleared by the baseline as well, so those criteria alone do not separate the arms; and the
          stage ranking resolves a <em>grouping</em> (photometric ahead of the rest), not a strict 1-to-7 order.
        </div>
      </Sec>

      <Sec title="EH-3 Dominance Criterion">
        <DataTable
          headers={['Criterion', 'ResNet-50 (B−A)', 'EfficientNet-B3 (D−C)', 'Threshold']}
          rows={[
            ['ΔF1', `+${((CONFIGS.B.f1 - CONFIGS.A.f1) * 100).toFixed(2)}pp ✓`, `+${((CONFIGS.D.f1 - CONFIGS.C.f1) * 100).toFixed(2)}pp ✓`, '≥ 5pp'],
            ['ΔAUC', `+${((CONFIGS.B.auc - CONFIGS.A.auc) * 100).toFixed(2)}pp ✓`, `+${((CONFIGS.D.auc - CONFIGS.C.auc) * 100).toFixed(2)}pp ✓`, '≥ 2pp'],
            ['Δκ', `+${((CONFIGS.B.k - CONFIGS.A.k) * 100).toFixed(2)}pp ✓`, `+${((CONFIGS.D.k - CONFIGS.C.k) * 100).toFixed(2)}pp ✓`, '> 0'],
          ]}
          highlightRow={(row, i) => i === 0}
        />
      </Sec>
    </div>
  );
}

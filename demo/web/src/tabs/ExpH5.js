import { C, ALO, IOU, ALO_DIRECTION, ALO_THRESHOLD } from '../data';
import { Sec, DataTable, Paired, Hbar, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ExpH5() {
  const { t } = useLang();
  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, margin: '0 0 4px 0', color: 'var(--color-text-primary,#222)' }}>
          H-5: Explainability (ALO) Hypothesis
        </h2>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary,#666)' }}>
          Experiment 4 — Grad-CAM attention analysis with EfficientNet-B3 on all 54 IDRiD images carrying lesion masks (τ = 0.5)
        </div>
      </div>

      <Sec title={t('exp.alo')}>
        <Paired
          items={ALO.map(d => ({ label: d.l, a: d.ab, b: d.ap }))}
          c1={C.gray}
          c2={C.teal}
          l1="Baseline"
          l2="Pipeline"
        />
        <DataTable
          headers={['Lesion Type', 'n', 'Baseline ALO', 'Pipeline ALO', 'ΔALO', '95% CI (Δ)', 'p (Wilcoxon, 1-sided)', 'Relative']}
          rows={ALO.map(d => [
            d.l,
            d.n,
            d.ab.toFixed(4),
            d.ap.toFixed(4),
            `+${(d.ap - d.ab).toFixed(4)}`,
            `[+${d.ci[0].toFixed(4)}, +${d.ci[1].toFixed(4)}]`,
            `${d.p.toFixed(4)} ✓`,
            `+${((d.ap - d.ab) / d.ab * 100).toFixed(0)}%`,
          ])}
        />
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp4/06_exp4_alo.png'} caption="ALO (Attention-Lesion Overlap) by lesion type across all 54 mask-carrying IDRiD images. The pipeline raises ALO on all 4 types, and all 4 differences are statistically significant (p 0.0007–0.0148)." figNum={6} tooltip="tooltip.fig06" />
        <Note>
          ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask). Primary explainability metric.
          Preprocessing improves ALO by +37–49% and every difference is significant, with all four 95% CIs excluding zero.
          Hard exudates gain most in absolute terms (+0.1288; bright, well-defined boundary → strong contrast response after CLAHE).
          Soft exudates carry the weakest significance (p = 0.0148) simply because only 26 of the 54 images are annotated for them.
          <strong> INVARIANTS NC-14 still applies:</strong> this measures alignment of attention with annotated lesions, not
          clinical localization of pathology — the model is not "finding lesions".
        </Note>
      </Sec>

      <Sec title={t('exp.iou')}>
        <Paired
          items={IOU.map(d => ({ label: d.l, a: d.baseline, b: d.pipeline }))}
          c1={C.gray}
          c2={C.purple}
          l1="Baseline"
          l2="Pipeline"
        />
        <DataTable
          headers={['Lesion Type', 'Baseline IoU', 'Pipeline IoU', 'ΔIoU', 'p (Wilcoxon, 1-sided)']}
          rows={IOU.map(d => [
            d.l,
            d.baseline.toFixed(4),
            d.pipeline.toFixed(4),
            `+${(d.pipeline - d.baseline).toFixed(4)}`,
            `${d.p.toFixed(4)} ✓`,
          ])}
        />
        <ImageWithTooltip src={process.env.PUBLIC_URL + '/results/exp4/07_exp4_iou.png'} caption="IoU (Intersection over Union) by lesion type. IoU values are lower than ALO due to stricter penalization of activation outside lesion boundaries. Pipeline consistently improves IoU across all lesion types." figNum={7} tooltip="tooltip.fig07" />
        <Note>
          IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask). Secondary metric — stricter than ALO
          because it penalizes excessive activation outside lesions. Lower absolute values are expected since Grad-CAM
          activations are inherently diffuse. The pipeline reduces off-lesion activation by suppressing non-diagnostic
          image regions through flat-field correction and CLAHE. IoU agrees with ALO on all four types
          (+46–59% relative, p = 0.0011–0.0189), so the secondary metric does not contradict the primary one.
        </Note>
      </Sec>

      <Sec title={t('exp.aloImprovement')}>
        <Hbar
          items={ALO.map(d => ({
            label: d.l,
            v: parseFloat(((d.ap - d.ab) / d.ab * 100).toFixed(1)),
            color: C.coral,
          }))}
          maxV={75}
        />
      </Sec>

      <Sec title="Per-Image Direction of the Effect">
        <DataTable
          headers={['Lesion Type', 'n', '↑ better with pipeline', '↓ worse', '= unchanged', 'share ↑']}
          rows={ALO_DIRECTION.map(d => [
            d.l, d.n, d.up, d.down, d.same, `${(d.up / d.n * 100).toFixed(0)}%`,
          ])}
        />
        <Note>
          The effect holds at the level of individual images rather than resting on a few outliers: 65–76% of images
          improve against 9–15% that get worse. The mean shifts therefore reflect a consistent movement of the
          majority. Floor effect is minor — only 6 of 54 images have ALO = 0 in <em>both</em> arms (f₀ = 0.111),
          so the measurement operates inside the metric's working range.
        </Note>
      </Sec>

      <Sec title="Robustness to the Binarization Threshold">
        <DataTable
          headers={['τ (heat-map threshold)', 'Types improved', 'Types significant (p < 0.05)']}
          rows={ALO_THRESHOLD.map(d => [
            d.tau === 0.5 ? `${d.tau.toFixed(1)} (canonical)` : d.tau.toFixed(1),
            `${d.improved} / 4`,
            `${d.significant} / 4`,
          ])}
          highlightRow={(row, i) => ALO_THRESHOLD[i].tau === 0.5}
        />
        <Note>
          The direction survives at every threshold from 0.2 to 0.7; significance is lost for exactly one lesion type
          at the strictest τ = 0.7, where the activated area is smallest. The result is therefore not an artefact of
          choosing the canonical τ = 0.5.
        </Note>
      </Sec>
    </div>
  );
}

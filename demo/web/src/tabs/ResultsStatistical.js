import { C, STAT_TESTS, TRAIN_TEST_GAP } from '../data';
import { Sec, DataTable, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ResultsStatistical() {
  const { t } = useLang();
  return (
    <div>
      <Sec title={t('results.statTests')}>
        <DataTable
          headers={['Test', 'ResNet-50 (B vs A)', 'EfficientNet-B3 (D vs C)']}
          rows={STAT_TESTS.map(d => [d.test, d.resnet, d.effnet])}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/21_statistical_tests.png'}
          caption="Statistical test results visualized. Both architectures show a statistically significant preprocessing improvement: ResNet-50 (B−A, DeLong p=0.0041, McNemar p=0.0057) and EfficientNet-B3 (D−C, DeLong p=0.0028, McNemar p=0.0041). Bootstrap CIs exclude zero for both."
          figNum={21}
          tooltip="tooltip.fig21"
        />
        <Note>
          Both architectures are significant at α=0.05 on every test, and both survive the Holm correction across
          the 4 configurations — so significance is not an artefact of multiple testing.
          ResNet-50: DeLong p=0.0041, McNemar p=0.0057, Holm p_adj=0.0082.
          EfficientNet-B3: DeLong p=0.0028, McNemar p=0.0041, Holm p_adj=0.0056.
          The McNemar discordance is moderately imbalanced (2190/2010 and 2265/2075), i.e. the pipeline does not
          merely reshuffle errors — it yields a net positive balance.
          <br /><br />
          A note on magnitude: DeLong z ≈ 2.87–2.99 is a moderate but stable effect. State it as "significant at
          0.05 after Holm correction" — not as "p &lt; 10⁻⁴".
        </Note>
      </Sec>

      <Sec title="Mixed-Effects ANOVA Interpretation">
        <div style={{ fontSize: 12, lineHeight: 1.7, color: 'var(--color-text-primary,#333)' }}>
          <p style={{ margin: '0 0 10px 0' }}>
            A mixed-effects ANOVA was fitted with preprocessing (2 levels), architecture (2 levels), and their
            interaction as fixed effects, with fold as a random effect. Results:
          </p>
          <div style={{ background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 7, padding: '10px 14px', fontFamily: 'monospace', fontSize: 11, lineHeight: 1.8 }}>
            <div style={{ fontWeight: 700, color: C.gray }}>Interaction (preprocessing × architecture): p=0.31 (n.s.)</div>
          </div>
          <p style={{ margin: '10px 0 0 0' }}>
            The non-significant interaction (p=0.31) is the statistical form of "on both backbones": the size of the
            preprocessing effect does not depend on the architecture. The numbers agree — ΔF1 is +6.54pp on
            ResNet-50 and +6.55pp on EfficientNet-B3, matching to the second decimal.
          </p>
          <p style={{ margin: '10px 0 0 0' }}>
            Only the interaction term was recorded in this run; the main-effect p-values are not reported here, so
            they are not quoted. The per-arm effects are established directly by the paired DeLong/McNemar tests above.
          </p>
        </div>
      </Sec>

      <Sec title="Convergence and Overfitting">
        <DataTable
          headers={['Config', 'Arm', 'Best epochs (per fold)', 'Train loss', 'Val loss', 'Loss gap']}
          rows={TRAIN_TEST_GAP.map(d => [
            d.config, d.arm, d.bestEpochs, d.trainLoss.toFixed(3), d.valLoss.toFixed(3), d.gap.toFixed(3),
          ])}
          highlightRow={(row, i) => i === 1 || i === 3}
        />
        <Note>
          The pipeline arms (B, D) converge roughly 7 epochs earlier (best epochs 7–10 vs 14–17) and hold a
          2.5× smaller loss gap (0.021–0.022 vs 0.052–0.054). The mechanism is visible in the components: B and D
          have a <strong>higher</strong> train loss (0.126–0.131 vs 0.098–0.102) at comparable validation loss —
          they fit the training set less well yet generalize at least as well. That is regularizer behaviour: the
          4th channel and the illumination normalization shrink the hypothesis space by removing variation that
          carries no diagnostic signal. Best-epoch spread within an arm is ±1–1.5 epochs, so the regime is
          reproducible across folds rather than a lucky seed. Patient-level CV prevents leakage via bilateral pairs.
        </Note>
      </Sec>
    </div>
  );
}

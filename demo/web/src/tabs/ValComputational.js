import { COMPUTE } from '../data';
import { Sec, DataTable, Note, ImageWithTooltip } from '../components';
import { useLang } from '../i18n';

export default function ValComputational() {
  const { t } = useLang();
  return (
    <div>
      <Sec title={t('compute.efficiency')}>
        <DataTable
          headers={['Metric', 'ResNet-50', 'EfficientNet-B3', 'Unit']}
          rows={COMPUTE.map(d => [d.metric, d.resnet, d.effnet, d.unit])}
        />
        <ImageWithTooltip
          src={process.env.PUBLIC_URL + '/results/general/17_computational.png'}
          caption="Computational cost comparison: FLOPs, inference latency and GPU memory for ResNet-50 and EfficientNet-B3, measured on an RTX 3060 at 512×512, fp32. The 4th channel costs +0.4 GFLOPs (+0.9%) and +24 MiB."
          figNum={17}
          tooltip="tooltip.fig17"
        />
        <Note>
          <strong>The 4th channel is essentially free.</strong> Going from the 3-channel baseline to the 4-channel
          pipeline costs +0.4 GFLOPs (+0.9%), +24 MiB of VRAM and about +3k parameters (rounding to the same
          23.52M / 10.70M) — against a +6.55pp weighted-F1 gain. This is the quantitative form of the "cheap prior"
          claim: the pipeline's cost lives in CPU preprocessing, not in the network.
          <br /><br />
          <strong>FLOPs ≠ latency.</strong> EfficientNet-B3 is 4.3× cheaper in FLOPs (10 vs 43) and 2.2× lighter in
          parameters, yet only ~9% faster at bs=16 and actually <em>slower</em> at bs=1 (12.8–14.5 vs 10.5 ms):
          depthwise convolutions use tensor cores poorly. Any performance-complexity argument must be made on
          measured time, not on FLOPs.
          <br /><br />
          <strong>Training VRAM is the real bottleneck, and it is EfficientNet's.</strong> 13.7 GiB vs 3.7 GiB for
          ResNet-50 (fp32 without AMP, large 512² activation maps) — above the RTX 3060's physical 12 GiB, so the
          measurement only completed via WSL2/WDDM host-memory sharing. The batch_size = 16 limit is driven by fp32
          activations at 512², not by model size.
        </Note>
      </Sec>

      <Sec title="Hardware Configuration">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {[
            { label: 'GPU', value: 'NVIDIA RTX 3060 12GB VRAM' },
            { label: 'OS', value: 'WSL2 Ubuntu 22.04 on Windows 11' },
            { label: 'Framework', value: 'PyTorch 2.5, CUDA 12.x' },
            { label: 'Python', value: '3.10, Conda environment' },
            { label: 'Input resolution', value: '512×512 RGB' },
            { label: 'Mixed precision', value: 'Enabled for ResNet-50; disabled for EfficientNet (fp16 overflow)' },
          ].map((item, i) => (
            <div key={i} style={{ display: 'flex', gap: 10, padding: '6px 12px', background: 'var(--color-background-secondary,#f7f7f5)', borderRadius: 5 }}>
              <div style={{ minWidth: 140, fontWeight: 600, fontSize: 11 }}>{item.label}</div>
              <div style={{ fontSize: 11, color: 'var(--color-text-primary,#333)' }}>{item.value}</div>
            </div>
          ))}
        </div>
      </Sec>

      <Sec title="Network Throughput">
        <Note>
          Measured with the standard <code>torch.utils.flop_counter</code>, 50 iterations after 10 warm-up runs;
          the train step is fwd + bwd + optimizer.step under the same mixed-precision setting each configuration was
          trained with. At bs=16 the pipeline arms reach 120.5 img/s (ResNet-50) and 132.3 img/s (EfficientNet-B3).
          <br /><br />
          <strong>Not measured:</strong> the wall-clock cost of the CPU preprocessing stages themselves, and
          training time per epoch. Those figures are not part of this benchmark and are therefore not quoted here.
        </Note>
      </Sec>
    </div>
  );
}

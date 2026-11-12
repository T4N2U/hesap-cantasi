"""Original 'playful plucks' background track, synthesised from scratch (no samples, no copyright)."""
import numpy as np, wave, sys
SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 59.0
BPM = 112; BEAT = 60 / BPM; STEP = BEAT / 2  # eighth notes
N = int(SR * DUR)
out = np.zeros((N, 2))

def note_hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def marimba(m, length=0.45, vel=1.0):
    t = np.arange(int(SR * length)) / SR
    f = note_hz(m)
    env = np.exp(-t * 9) * (1 - np.exp(-t * 400))
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30) + 0.12 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t * 60)
    return s * env * vel

def pluck_bass(m, length=0.5, vel=1.0):
    t = np.arange(int(SR * length)) / SR
    f = note_hz(m)
    env = np.exp(-t * 6) * (1 - np.exp(-t * 300))
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * env * vel

def shaker(length=0.06, vel=1.0):
    n = int(SR * length); x = np.random.default_rng(len(out)).standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))  # crude high-pass
    return x * np.exp(-np.arange(n) / SR * 70) * vel

def knock(length=0.12, vel=1.0):
    t = np.arange(int(SR * length)) / SR
    f = 160 * np.exp(-t * 25) + 55
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28) * vel

def add(sig, t0, pan=0.0, gain=1.0):
    i = int(t0 * SR)
    if i >= N: return
    seg = sig[: N - i] * gain
    out[i:i + len(seg), 0] += seg * (1 - pan) / 2 * 2 ** 0.5 * 0.7
    out[i:i + len(seg), 1] += seg * (1 + pan) / 2 * 2 ** 0.5 * 0.7

# I – vi – IV – V in C major; each chord 2 bars of 4/4
chords = [(60, [60, 64, 67, 72]), (57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (55, [55, 59, 62, 67])]
# playful arpeggio pattern per bar (indices into chord tones, None = rest)
pattern = [0, 2, 1, 3, None, 2, 3, 1]
melody = [[76, None, 79, 76, 74, None, 72, None], [74, 76, None, 72, None, 69, 72, None],
          [72, None, 74, 72, 69, None, 67, None], [71, 72, 74, None, 79, None, 77, 74]]
rng = np.random.default_rng(7)
bar_len = BEAT * 4
t = 0.0; bar = 0
while t < DUR:
    ci = (bar // 2) % 4
    root, tones = chords[ci]
    section = int(t // (bar_len * 8))  # changes every 8 bars
    for s, idx in enumerate(pattern):
        ts = t + s * STEP + (0.012 if s % 2 else 0)  # tiny swing
        if idx is not None:
            add(marimba(tones[idx] + 12, vel=0.55 + 0.1 * rng.random()), ts, pan=-0.35 + 0.7 * (s / 7), gain=0.5)
        add(shaker(vel=0.5 if s % 2 else 0.25), ts, pan=0.4, gain=0.18)
    # bass on beats 1 and 3, little pickup on the 'and' of 4
    add(pluck_bass(root - 24, 0.6), t, gain=0.6)
    add(pluck_bass(root - 24 + 7, 0.4), t + 2 * BEAT, gain=0.45)
    add(pluck_bass(root - 24 + 12, 0.2), t + 3.5 * BEAT, gain=0.3)
    add(knock(), t, gain=0.35); add(knock(), t + 2 * BEAT, gain=0.25)
    # melody plays in bars 9+ (after the intro), lighter in the final section
    if bar >= 8:
        for s, m in enumerate(melody[ci]):
            if m is not None and (bar % 2 == 0 or s < 4):
                add(marimba(m, 0.6, 0.8), t + s * STEP, pan=0.15, gain=0.42)
    t += bar_len; bar += 1

# gentle room reverb (a few feedback delays) for warmth
for d, g in [(0.083, 0.25), (0.131, 0.18), (0.211, 0.12)]:
    k = int(d * SR)
    out[k:] += out[:-k] * g

# fades and normalisation
fi, fo = int(1.0 * SR), int(2.5 * SR)
out[:fi] *= np.linspace(0, 1, fi)[:, None]
out[-fo:] *= np.linspace(1, 0, fo)[:, None]
out /= np.max(np.abs(out)) / 0.89
pcm = (out * 32767).astype('<i2')
with wave.open(sys.argv[2] if len(sys.argv) > 2 else 'music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', DUR)

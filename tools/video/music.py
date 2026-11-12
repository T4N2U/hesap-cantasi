"""Hesap Çantası background music: one signature melody, many arrangements.

Every video uses the same chord progression and melody (the channel's audio identity),
arranged with a different instrument set and rhythm. All presets are deliberately "safe":
moderate tempo, soft attacks, no harsh highs, gentle drums, same loudness after normalising.

Usage:  python3 music.py DURATION OUT.wav PRESET
Presets: playful-marimba, lofi-piano, acoustic-pluck, rhodes-groove, musicbox-light, soft-pad
"""
import sys, wave
import numpy as np

SR = 44100
CHORDS = [(60, [60, 64, 67, 72]), (57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (55, [55, 59, 62, 67])]  # I vi IV V in C
MELODY = [[76, None, 79, 76, 74, None, 72, None], [74, 76, None, 72, None, 69, 72, None],
          [72, None, 74, 72, 69, None, 67, None], [71, 72, 74, None, 79, None, 77, 74]]

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def tt(sec): return np.arange(int(SR * sec)) / SR

# ---------------- instruments (all mono, peak ~1) ----------------
def marimba(m, L=0.45):
    t = tt(L); f = hz(m)
    return (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*4*f*t)*np.exp(-t*30)) * np.exp(-t*9) * (1-np.exp(-t*400))

def piano(m, L=1.2):
    t = tt(L); f = hz(m)
    s = sum(a*np.sin(2*np.pi*f*k*t*(1+0.0004*k*k)) for k, a in [(1, 1), (2, .45), (3, .22), (4, .1), (5, .05)])
    return s * (0.7*np.exp(-t*2.2) + 0.3*np.exp(-t*7)) * (1-np.exp(-t*300)) / 1.6

def pluck(m, L=0.9):  # Karplus-Strong nylon-like guitar
    f = hz(m); n = int(SR * L); p = max(2, int(SR / f))
    rng = np.random.default_rng(m)
    buf = rng.uniform(-1, 1, p); out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    # soften: one-pole lowpass
    y = np.empty(n); acc = 0.0
    for i in range(n): acc += 0.35 * (out[i] - acc); y[i] = acc
    return y / (np.max(np.abs(y)) + 1e-9)

def rhodes(m, L=1.0):  # 2-operator FM electric piano
    t = tt(L); f = hz(m)
    idx = 1.4 * np.exp(-t*5)
    s = np.sin(2*np.pi*f*t + idx*np.sin(2*np.pi*f*t)) + 0.15*np.sin(2*np.pi*14*f*t)*np.exp(-t*40)
    return s * np.exp(-t*2.8) * (1-np.exp(-t*250)) / 1.15

def musicbox(m, L=0.9):
    t = tt(L); f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*10) + 0.12*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*25)
    return s * np.exp(-t*4) * (1-np.exp(-t*600)) / 1.3

def pad(m, L=2.2):
    t = tt(L); f = hz(m)
    s = sum(np.sin(2*np.pi*f*d*t + ph) for d, ph in [(1, 0), (1.004, 1.1), (0.996, 2.3), (2.002, .4)])
    env = np.minimum(1, t/0.6) * np.minimum(1, (L - t)/0.8)
    return s * env / 4

def bass(m, L=0.5):
    t = tt(L); f = hz(m)
    return (np.sin(2*np.pi*f*t) + 0.2*np.sin(2*np.pi*2*f*t)) * np.exp(-t*5) * (1-np.exp(-t*250))

def kick(L=0.25):
    t = tt(L); f = 120*np.exp(-t*30) + 45
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*14)

def snare(L=0.18, seed=1):
    n = int(SR*L); x = np.random.default_rng(seed).standard_normal(n)
    x = np.convolve(x, np.ones(6)/6, 'same')  # soften
    t = np.arange(n)/SR
    return (x*0.6 + 0.4*np.sin(2*np.pi*190*t)) * np.exp(-t*22)

def shaker(L=0.06, seed=2):
    n = int(SR*L); x = np.diff(np.concatenate([[0], np.random.default_rng(seed).standard_normal(n)]))
    return x * np.exp(-np.arange(n)/SR*70)

# ---------------- presets: instruments + rhythm ----------------
# arp: pattern of chord-tone indices per eighth (None = rest); swing in seconds; drums: which hits
PRESETS = {
    'playful-marimba': dict(bpm=112, swing=0.012, chord_inst=marimba, chord_oct=12, arp=[0, 2, 1, 3, None, 2, 3, 1], arp_gain=.5,
                            lead=marimba, lead_gain=.42, drums='shaker-knock', bass=True),
    'lofi-piano':      dict(bpm=84, swing=0.05, chord_inst=piano, chord_oct=0, arp='block', arp_gain=.42,
                            lead=piano, lead_gain=.36, drums='lofi', bass=True, vinyl=True),
    'acoustic-pluck':  dict(bpm=100, swing=0.0, chord_inst=pluck, chord_oct=0, arp=[0, 2, 3, 2, 1, 2, 3, 2], arp_gain=.42,
                            lead=pluck, lead_gain=.40, drums='shaker', bass=True),
    'rhodes-groove':   dict(bpm=96, swing=0.025, chord_inst=rhodes, chord_oct=0, arp=[0, None, None, 1, None, 2, None, None], arp_gain=.5,
                            lead=rhodes, lead_gain=.36, drums='soft-pop', bass=True),
    'musicbox-light':  dict(bpm=104, swing=0.0, chord_inst=musicbox, chord_oct=12, arp=[0, 1, 2, 3, 2, 1, 2, 3], arp_gain=.34,
                            lead=musicbox, lead_gain=.36, drums=None, bass=False, padbed=True),
    'soft-pad':        dict(bpm=90, swing=0.0, chord_inst=pad, chord_oct=0, arp='pad', arp_gain=.38,
                            lead=musicbox, lead_gain=.30, drums='heartbeat', bass=True),
}

def render(dur, preset):
    P = PRESETS[preset]; N = int(SR*dur); out = np.zeros((N, 2))
    beat = 60 / P['bpm']; step = beat / 2; bar = beat * 4
    def add(sig, t0, pan=0.0, g=1.0):
        i = int(t0*SR)
        if i >= N or t0 < 0: return
        s = sig[:N-i]*g
        out[i:i+len(s), 0] += s*(1-pan)*0.7; out[i:i+len(s), 1] += s*(1+pan)*0.7
    rng = np.random.default_rng(11)
    t = 0.0; b = 0
    while t < dur:
        root, tones = CHORDS[(b // 2) % 4]
        sw = lambda s: t + s*step + (P['swing'] if s % 2 else 0)
        if P['arp'] == 'block':          # lo-fi: chord on 1 and the 'and' of 2
            for off in (0, 1.5*beat):
                for k, n in enumerate(tones): add(P['chord_inst'](n + P['chord_oct']), t+off+k*0.012, pan=-.2+.13*k, g=P['arp_gain']*.55)
        elif P['arp'] == 'pad':          # sustained chord each bar
            if b % 2 == 0:
                for n in tones: add(pad(n, bar*2+0.6), t, pan=0, g=P['arp_gain'])
        else:
            for s, idx in enumerate(P['arp']):
                if idx is not None: add(P['chord_inst'](tones[idx] + P['chord_oct']), sw(s), pan=-.3+.6*(s/7), g=P['arp_gain']*(0.9+0.1*rng.random()))
        if P.get('padbed') and b % 2 == 0:
            for n in tones[:3]: add(pad(n - 12, bar*2+0.6), t, g=0.16)
        if P['bass']:
            add(bass(root-24, .6), t, g=.55); add(bass(root-24+7, .4), t+2*beat, g=.42)
        d = P['drums']
        if d == 'shaker-knock':
            for s in range(8): add(shaker(seed=s), sw(s), pan=.4, g=.17 if s % 2 else .09)
            add(kick()*.6, t, g=.35); add(kick()*.6, t+2*beat, g=.25)
        elif d == 'lofi':
            add(kick(), t, g=.42); add(kick(), t+2.5*beat, g=.3)
            add(snare(seed=b), t+beat+P['swing'], g=.2); add(snare(seed=b+7), t+3*beat+P['swing'], g=.2)
            for s in range(8): add(shaker(seed=s+b), sw(s), pan=.3, g=.06)
        elif d == 'shaker':
            for s in range(8): add(shaker(seed=s), sw(s), pan=.35, g=.14 if s % 2 else .08)
        elif d == 'soft-pop':
            for k in range(4): add(kick(), t+k*beat, g=.3)
            add(snare(seed=b), t+beat, g=.16); add(snare(seed=b+3), t+3*beat, g=.16)
        elif d == 'heartbeat':
            add(kick(), t, g=.28); add(kick(), t+0.28, g=.18)
        if b >= 8:  # melody enters after the intro, phrases alternate full/half
            for s, m in enumerate(MELODY[(b // 2) % 4]):
                if m is not None and (b % 2 == 0 or s < 4):
                    add(P['lead'](m), sw(s), pan=.12, g=P['lead_gain'])
        t += bar; b += 1
    if P.get('vinyl'):
        noise = np.random.default_rng(5).standard_normal(N) * 0.006
        out += np.convolve(noise, np.ones(30)/30, 'same')[:, None]
    for dly, g in [(0.083, .22), (0.131, .16), (0.211, .11)]:  # small room
        k = int(dly*SR); out[k:] += out[:-k]*g
    fi, fo = int(1.0*SR), int(2.5*SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]; out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return out / (np.max(np.abs(out)) / 0.89)

if __name__ == '__main__':
    dur = float(sys.argv[1]); path = sys.argv[2]; preset = sys.argv[3] if len(sys.argv) > 3 else 'playful-marimba'
    pcm = (render(dur, preset) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print('ok', preset, dur)

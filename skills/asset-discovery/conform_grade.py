#!/usr/bin/env python3
"""真实素材 → 成片底片：裁可用区间、统一 1920×1080@30、S2 调色匹配到 S1（Lab 均值方差 → 17³ .cube → ffmpeg lut3d）。
时刻来自 src/timeline.ts 的 SHOTS（这里用正则读，避免两处写数）。输出 public/plates/S*.mp4、out/lab/match.cube、out/lab/stats.json。"""
import json, re, subprocess, numpy as np
from pathlib import Path

TL = Path('src/timeline.ts').read_text()
SH = {m[0]: dict(src=m[1], inn=float(m[2]), dur=float(m[3])) for m in
      re.findall(r"(S\d): \{src: '([^']+)', in: ([\d.]+), dur: ([\d.]+)", TL)}
W, H, FPS = 1920, 1080, 30
VF = f'setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1'


def run(*a): subprocess.run(a, check=True)


def cut(k, extra='', out=None):
    s = SH[k]; out = out or f'public/plates/{k}.mp4'
    mi = 'minterpolate' in extra  # 多读 0.3 s、输出截到整段：minterpolate 会吃尾部 2 帧，VFR 源转 30 fps 出点会少 1 帧
    run('ffmpeg', '-y', '-loglevel', 'error', '-ss', str(s['inn']), '-t', str(s['dur'] + 0.3), '-i', s['src'],
        '-vf', f"{VF},{extra}" if mi else f"{VF},{extra}fps={FPS}", '-t', str(s['dur']),
        '-an', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
        '-color_trc', 'bt709', '-colorspace', 'bt709', out)
    return out


def frames(path, step=6, w=480, h=270):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-vf', f'select=not(mod(n\\,{step})),scale={w}:{h}',
                          '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)


def dupes(path):
    """相邻帧几乎相同（平均绝对差 < 0.5/255）的帧数：帧率上变换的重复帧。"""
    f = frames(path, step=1, w=320, h=180)
    return int((np.abs(np.diff(f, axis=0)).mean(axis=(1, 2, 3)) < 0.5).sum()), len(f)


# ---- Lab（与 effects/snippets/post-lab/lab.py 同一套公式）----
def srgb2lin(c): c = c / 255; return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lin2srgb(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255
M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]); WP = np.array([0.95047, 1, 1.08883])
def rgb2lab(rgb):
    xyz = srgb2lin(rgb) @ M.T / WP; f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
def lab2rgb(lab):
    fy = (lab[..., 0] + 16) / 116; fx = fy + lab[..., 1] / 500; fz = fy - lab[..., 2] / 200
    f = np.stack([fx, fy, fz], -1); xyz = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787) * WP
    return lin2srgb(xyz @ np.linalg.inv(M).T)


def stat(fr):
    lab = rgb2lab(fr).reshape(-1, 3)
    return lab.mean(0), lab.std(0)


Path('out/lab').mkdir(parents=True, exist_ok=True)
s1 = cut('S1')
s2raw = cut('S2', out='out/lab/S2_ungraded.mp4')
s2mi = cut('S2', extra=f'minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1', out='out/lab/S2_minterp.mp4')

r, t = frames(s1), frames(s2raw)
mu_r, sd_r = stat(r); mu_t, sd_t = stat(t)
ALPHA = 0.8  # 方差只迁移 80%：两镜内容不同（S2 天空更大），全量迁移会把对比压过头
sd_goal = sd_t + (sd_r - sd_t) * ALPHA
def transfer(rgb): lab = rgb2lab(rgb); return lab2rgb((lab - mu_t) / (sd_t + 1e-6) * sd_goal + mu_r)

n = 17; g = np.linspace(0, 255, n)
bgr = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1)
lut = transfer(bgr[..., ::-1].reshape(-1, 3)).reshape(n, n, n, 3) / 255
with open('out/lab/match.cube', 'w') as fh:
    fh.write(f'TITLE "S2 to S1 (Lab mean/std transfer)"\nLUT_3D_SIZE {n}\n')
    for c in lut.reshape(-1, 3): fh.write(f'{c[0]:.5f} {c[1]:.5f} {c[2]:.5f}\n')
# S2 源片 25 fps：用光流补帧版（重复帧 0；水花自带运动模糊，补帧伪影看不出）再套 LUT
run('ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/lab/S2_minterp.mp4', '-vf', 'lut3d=out/lab/match.cube:interp=tetrahedral',
    '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
    'public/plates/S2.mp4')

mu_g, sd_g = stat(frames('public/plates/S2.mp4'))
d = lambda a, b: float(np.linalg.norm(a - b))
info = {
    'S1': {'labMean': mu_r.round(2).tolist(), 'labStd': sd_r.round(2).tolist()},
    'S2_before': {'labMean': mu_t.round(2).tolist(), 'labStd': sd_t.round(2).tolist()},
    'S2_after': {'labMean': mu_g.round(2).tolist(), 'labStd': sd_g.round(2).tolist()},
    'meanDeltaE_before': round(d(mu_t, mu_r), 2), 'meanDeltaE_after': round(d(mu_g, mu_r), 2),
    'alpha': ALPHA,
    'dupFrames': {'S1_fps30': dupes(s1), 'S2_fps30': dupes(s2raw), 'S2_minterp': dupes(s2mi)},
}
json.dump(info, open('out/lab/stats.json', 'w'), indent=1)
print(json.dumps(info, indent=1))

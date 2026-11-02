#!/usr/bin/env python3
"""成片逐帧核验：每帧与它应取的底片帧在无字幕区（画面上部中央）比对，差值异常即坏帧（取帧错位、解码马赛克）。
用法：python3 -I scripts/check_frames.py out/silent.mp4   退出码 1 = 有坏帧"""
import re, subprocess, sys, numpy as np
from pathlib import Path

TL = Path('src/timeline.ts').read_text()
cut = float(re.search(r'cut: ([\d.]+)', TL)[1])
W, H = 480, 270


def fr(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


F = fr(sys.argv[1]); P = np.concatenate([fr('public/plates/S1.mp4'), fr('public/plates/S2.mp4')])
roi = lambda a: a[..., 30:120, 120:360]
d = np.abs(roi(F) - roi(P[:len(F)])).mean(axis=(1, 2))
fade = int(len(F) - 0.5 * 30)  # 片尾淡出段不比
med = np.median(d[:fade]); bad = [i for i in range(fade) if d[i] > max(15, 3 * med)]
print(f'{sys.argv[1]}: {len(F)} 帧，与底片差中位 {med:.2f}，坏帧 {len(bad)} 个 {bad[:20]}')
sys.exit(1 if bad else 0)

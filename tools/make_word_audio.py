#!/usr/bin/env python3
"""スワヒリ語の単語帳の発音（🔊）の音声を作る。iPhone などスワヒリ語の声がない端末でも聞けるように、mp3 で置いておく。

    python tools/make_word_audio.py --model sw_CD-lanfrica-medium.onnx   # 足りない分だけ作る（いらなくなった分は消す）

books/swahili/words/*.txt の単語ごとに books/swahili/audio/<名前>.mp3 を作る。
<名前> は単語の欄を小文字にして、a-z と 0-9 以外を「-」にしたもの（index.html の wordAudio と同じ。mtu（watu） → mtu-watu）。
読むのは単語と、（ ）の複数の形（「mtu, watu」）。形容詞の頭の「-」は読まない。

声は Piper の sw_CD-lanfrica-medium（男性の声）を、Praat の Change gender で女性の高さ（約210 Hz）にしたもの（本人が選んだ）。
いるもの（scratchpad の venv などに）: pip install piper-tts lameenc praat-parselmouth
モデル: https://huggingface.co/rhasspy/piper-voices/tree/main/sw/sw_CD/lanfrica/medium の .onnx と .onnx.json
"""
import argparse
import re
import unicodedata
from pathlib import Path

import lameenc
import numpy as np
import parselmouth
from parselmouth.praat import call
from piper import PiperVoice, SynthesisConfig

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "swahili"
PITCH, FORMANT = 210, 1.17      # 女性の声の高さ（Hz）と、声の響き（フォルマント）を上げる割合
SPEED = 1.1                     # 1 より大きいとゆっくり


def slug(w):
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", w).lower()).strip("-")


def spoken(w):
    s = re.sub(r"\s*[（(]([^）)]*)[）)]", r", \1", w)      # mtu（watu） → mtu, watu
    s = re.sub(r"(^|[\s,])-", r"\1", s)                     # -zuri → zuri
    return s.replace("…", "").strip()


def words():
    out = {}
    for f in sorted((BOOK / "words").glob("*.txt")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or "|" not in line:
                continue
            w = line.split("|")[0].strip()
            k = slug(w)
            if k in out and spoken(out[k]).lower().rstrip("?!.") != spoken(w).lower().rstrip("?!."):
                print(f"同じ名前になる: {out[k]} と {w}（{k}）")
            out.setdefault(k, w)
    return out


def synth(voice, text):
    sr = voice.config.sample_rate
    pcm = b"".join(c.audio_int16_bytes for c in voice.synthesize(text, syn_config=SynthesisConfig(length_scale=SPEED)))
    a = np.frombuffer(pcm, dtype=np.int16).astype(np.float64) / 32768
    x = call(parselmouth.Sound(a, sampling_frequency=sr), "Change gender", 75, 400, FORMANT, PITCH, 1.0, 1.0).values[0]
    loud = np.flatnonzero(np.abs(x) > 0.01)                  # 前後の無音を 0.08 秒だけ残して切る
    if len(loud):
        x = x[max(0, loud[0] - sr * 2 // 25): loud[-1] + sr * 2 // 25]
    x = x / max(1e-9, np.abs(x).max()) * 0.9
    e = lameenc.Encoder()
    e.set_bit_rate(48)
    e.set_in_sample_rate(sr)
    e.set_channels(1)
    e.set_quality(2)
    return e.encode((x * 32767).astype(np.int16).tobytes()) + e.flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="sw_CD-lanfrica-medium.onnx")
    ap.add_argument("--all", action="store_true", help="あるものも作り直す")
    args = ap.parse_args()
    ws = words()
    d = BOOK / "audio"
    d.mkdir(exist_ok=True)
    for f in d.glob("*.mp3"):
        if f.stem not in ws:
            f.unlink()
            print("消した:", f.name)
    voice = PiperVoice.load(args.model)
    todo = [k for k in ws if args.all or not (d / f"{k}.mp3").exists()]
    for i, k in enumerate(todo, 1):
        (d / f"{k}.mp3").write_bytes(synth(voice, spoken(ws[k])))
        if i % 200 == 0 or i == len(todo):
            print(f"{i}/{len(todo)}")
    print(f"{len(ws)} 語（作った {len(todo)}）")


if __name__ == "__main__":
    main()

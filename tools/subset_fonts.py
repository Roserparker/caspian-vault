#!/usr/bin/env python3
"""Caspian Vault 字体子集化（方案一：仿宋作题·今楷为文·文楷作注·Lora 西文）
改动 index.html 文案后重跑本脚本，再 commit fonts/。
源字体路径按本机调整。"""
import re, subprocess, sys, os, string

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
OUT  = os.path.join(ROOT, "fonts")
os.makedirs(OUT, exist_ok=True)

SRC = {
    "zhuque": "/Users/garfield/Downloads/BKB书籍/字体/ZhuqueFangsong-Regular.ttf",
    "jinkai": "/Users/garfield/Downloads/BKB书籍/字体/仓耳今楷05-W02.ttf",
    "wenkai": "/Users/garfield/Downloads/BKB书籍/字体/LXGWWenKaiGB-Regular.ttf",
    "lora":     "/Users/garfield/Downloads/Bitter,Lora/Lora/static/Lora-Regular.ttf",
    "lora-med": "/Users/garfield/Downloads/Bitter,Lora/Lora/static/Lora-Medium.ttf",
}

s = open(HTML, encoding="utf-8").read()
strip = lambda t: re.sub(r"<[^>]+>", "", t)

# ── 标题集（朱雀仿宋渲染的元素） ──
disp = []
disp += [strip(m) for m in re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", s, re.S)]
disp += [strip(m) for m in re.findall(r'class="hero-slogan"[^>]*>(.*?)</div>', s, re.S)]
disp += [strip(m) for m in re.findall(r'class="vd-step[^"]*"><b>(.*?)</b>', s, re.S)]
i = s.find("如果比特币归零")
if i > 0: disp.append(strip(s[i-40:i+400]))
disp.append("里海金库聚流成海，藏金于渊。先把最坏的话说在最前面")
DISP = "".join(sorted(set("".join(disp))))

# ── 小注集（霞鹜文楷渲染的元素） ──
note = []
note += [strip(m) for m in re.findall(r'<p class="note[^>]*>(.*?)</p>', s, re.S)]
note += [strip(m) for m in re.findall(r'<div class="fx">(.*?)</div>', s, re.S)]
note += [strip(m) for m in re.findall(r'class="cap">(.*?)</div>', s, re.S)]
note += [strip(m) for m in re.findall(r'class="commit[^"]*">(.*?)</div>', s, re.S)]
NOTE = "".join(sorted(set("".join(note))))

# ── 全集（仓耳今楷=正文兜底：整文件所有字符） ──
FULL = "".join(sorted(set(s)))
# ── 西文集 ──
LATIN = string.printable + "₿≈×−–—·「」％℃"

def subset(key, src, chars, out_name):
    cf = os.path.join(OUT, f"_{key}.chars.txt")
    open(cf, "w", encoding="utf-8").write(chars)
    out = os.path.join(OUT, out_name)
    r = subprocess.run([sys.executable, "-m", "fontTools.subset", src,
        f"--text-file={cf}", "--flavor=woff2", f"--output-file={out}",
        "--layout-features=*", "--no-hinting", "--desubroutinize"],
        capture_output=True, text=True)
    os.remove(cf)
    if r.returncode != 0:
        print(f"FAIL {key}: {r.stderr[-400:]}"); sys.exit(1)
    print(f"{out_name}: {os.path.getsize(out)//1024} KB ({len(set(chars))} 字符)")

subset("zhuque", SRC["zhuque"], DISP + LATIN, "zhuque.woff2")
subset("jinkai", SRC["jinkai"], FULL, "jinkai.woff2")
subset("wenkai", SRC["wenkai"], NOTE + LATIN, "wenkai.woff2")
subset("lora",   SRC["lora"],   LATIN, "lora.woff2")
subset("lora-med", SRC["lora-med"], LATIN, "lora-med.woff2")
print("done → fonts/")

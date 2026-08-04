#!/usr/bin/env python3
"""Build the ArmBench CI narrated Devpost demo video."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "video"
OUT.mkdir(exist_ok=True)
W, H = 1920, 1080
BG = "#07111f"
WHITE = "#f7fbff"
MUTED = "#a9bfd3"
CYAN = "#21d4fd"
PURPLE = "#8b5cf6"
GREEN = "#4ade80"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)

def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            line = trial
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def base(kicker, title, subtitle=""):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((70, 55, 390, 108), 20, fill="#102a43")
    d.text((95, 66), kicker.upper(), font=font(25, True), fill=CYAN)
    d.text((70, 145), title, font=font(66, True), fill=WHITE)
    if subtitle:
        for i, line in enumerate(wrap(d, subtitle, font(31), 1660)):
            d.text((74, 235 + i * 43), line, font=font(31), fill=MUTED)
    d.text((70, 1010), "ArmBench CI  •  Cloud AI  •  Native Arm64", font=font(24), fill="#6887a3")
    d.text((1680, 1010), "ILoveBuns", font=font(24, True), fill="#6887a3")
    return im, d

def card(d, xy, title, value, note="", accent=CYAN):
    x1,y1,x2,y2=xy
    d.rounded_rectangle(xy, 28, fill="#0e2035", outline="#23445f", width=2)
    d.text((x1+34,y1+30), title, font=font(25, True), fill=MUTED)
    d.text((x1+34,y1+77), value, font=font(50, True), fill=accent)
    if note: d.text((x1+34,y2-50), note, font=font(22), fill=MUTED)

def screenshot_slide(path, kicker, title, subtitle, image_path):
    im,d=base(kicker,title,subtitle)
    shot=Image.open(image_path).convert("RGB")
    shot.thumbnail((1680,650))
    panel=Image.new("RGB",(shot.width+20,shot.height+20),"#183047")
    panel.paste(shot,(10,10))
    im.paste(panel,((W-panel.width)//2,340))
    return im

slides=[]

im,d=base("Arm Create • Cloud AI", "ArmBench CI", "Reproducible FP32 vs INT8 ONNX benchmarking on native Arm64 CI")
d.rounded_rectangle((70,380,1850,890),35,fill="#0a1b2c",outline="#264d69",width=3)
for x,label,color in [(210,"TRAIN\nFP32",CYAN),(650,"EXPORT\nONNX",PURPLE),(1090,"QUANTIZE\nINT8",GREEN),(1510,"BENCHMARK\nARM64","#fbbf24")]:
    d.ellipse((x,500,x+170,670),fill="#122a40",outline=color,width=6)
    for j,line in enumerate(label.split("\n")):
        box=d.textbbox((0,0),line,font=font(28,True)); d.text((x+85-(box[2]-box[0])/2,535+j*42),line,font=font(28,True),fill=WHITE)
for x in (420,860,1300): d.line((x,585,x+130,585),fill="#54748f",width=8); d.polygon([(x+130,585),(x+105,570),(x+105,600)],fill="#54748f")
slides.append(im)

im,d=base("The problem", "Optimization needs evidence", "A smaller model is not automatically a better model. Size, speed, accuracy, and memory must be measured together on the target architecture.")
card(d,(90,410,590,820),"TARGET HARDWARE","Native Arm64","not an x86 estimate",CYAN)
card(d,(710,410,1210,820),"TRADE-OFFS","4 metric groups","size • accuracy • speed • RSS",PURPLE)
card(d,(1330,410,1830,820),"REPRODUCIBILITY","CI artifacts","JSON + Markdown + versions",GREEN)
slides.append(im)

slides.append(screenshot_slide(ROOT/"video-repo.png","Open source","One-command reproduction","Apache-2.0 source, pinned dependencies, workflow definition, and a committed reference report.",ROOT/"video-repo.png"))

im,d=base("Pipeline", "From training to an auditable report", "Every run records the architecture and software environment before comparing FP32 and dynamically quantized INT8 models.")
steps=[("1","Train","Deterministic intent classifier"),("2","Export","FP32 model to ONNX"),("3","Quantize","Dynamic INT8 weights"),("4","Measure","Accuracy, size, p50/p95, throughput, RSS"),("5","Publish","JSON, Markdown, workflow artifact")]
for i,(n,t,note) in enumerate(steps):
    y=370+i*118
    d.ellipse((100,y,172,y+72),fill=PURPLE)
    d.text((124,y+16),n,font=font(29,True),fill=WHITE)
    d.text((215,y+1),t,font=font(34,True),fill=WHITE)
    d.text((510,y+6),note,font=font(28),fill=MUTED)
    if i<4:d.line((136,y+74,136,y+112),fill="#405e79",width=5)
slides.append(im)

slides.append(screenshot_slide(ROOT/"video-run.png","Native execution","Public Arm64 workflow evidence","GitHub's ubuntu-24.04-arm runner reports aarch64 and produces downloadable benchmark artifacts.",ROOT/"video-run.png"))

im,d=base("Measured result", "INT8 trade-offs on native Arm64", "One reproducible hosted run. These are workload-specific measurements, not universal performance claims.")
card(d,(80,390,520,790),"MODEL SIZE","−73.39%","271.0 → 72.1 KiB",GREEN)
card(d,(550,390,990,790),"P50 LATENCY","1.07×","0.0139 → 0.0130 ms",CYAN)
card(d,(1020,390,1460,790),"THROUGHPUT","2.26×","median across 9 trials",PURPLE)
card(d,(1490,390,1840,790),"ACCURACY","−0.0075","0.4163 → 0.4088","#fbbf24")
d.text((110,850),"FP32",font=font(25,True),fill=MUTED); d.rectangle((220,852,810,880),fill="#38536b")
d.text((110,910),"INT8",font=font(25,True),fill=MUTED); d.rectangle((220,912,377,940),fill=GREEN)
slides.append(im)

im,d=base("CI as a gate", "Repeatable, inspectable, extensible", "The benchmark is intentionally small enough for standard CPU-only CI and can be replaced with larger ONNX workloads.")
features=[("Architecture proof","aarch64 platform details in every report"),("Regression-ready","machine-readable JSON for threshold checks"),("Transparent trade-offs","before/after metrics, including accuracy"),("Extensible","more models, runners, and quantization strategies")]
for i,(t,n) in enumerate(features):
    x=90+(i%2)*880; y=380+(i//2)*260
    d.rounded_rectangle((x,y,x+800,y+200),28,fill="#0e2035",outline="#254966",width=2)
    d.text((x+35,y+35),t,font=font(34,True),fill=CYAN if i%2==0 else PURPLE)
    for j,line in enumerate(wrap(d,n,font(27),720)):d.text((x+35,y+100+j*36),line,font=font(27),fill=MUTED)
slides.append(im)

slides.append(screenshot_slide(ROOT/"video-devpost.png","Submitted","ArmBench CI is ready for review","Cloud AI track submission with public source, native Arm64 evidence, benchmark artifacts, and reproducible instructions.",ROOT/"video-devpost.png"))

for i,im in enumerate(slides,1): im.save(OUT/f"slide-{i:02d}.png",quality=95)

narration=[
"ArmBench CI is a reproducible Cloud AI benchmark for the Arm Create AI Optimization Challenge. It turns an FP32 intent classifier into INT8 ONNX, then measures the result on native Arm64 hardware.",
"Optimization needs evidence. A smaller model is not automatically better. ArmBench CI evaluates model size, accuracy, latency, throughput, and process memory together, on the target architecture, with the full environment recorded.",
"The project is fully open source under Apache 2.0. The repository contains pinned dependencies, the benchmark and report renderer, the Arm64 GitHub Actions workflow, setup instructions, and a committed reference report.",
"The pipeline has five auditable stages. It trains a deterministic classifier, exports FP32 ONNX, performs dynamic INT8 quantization, measures both models, and publishes machine-readable JSON plus a readable Markdown artifact.",
"This is real native execution, not an emulated estimate. The public workflow uses GitHub's Ubuntu twenty four oh four Arm runner. The report records A arch sixty four, the Linux platform, CPU count, Python version, and ONNX Runtime version.",
"On the reference Arm64 run, INT8 reduced model size by seventy three point three nine percent. P fifty latency improved by one point zero seven times, throughput roughly doubled, and accuracy changed by minus zero point zero zero seven five. These are transparent, workload-specific trade-offs.",
"ArmBench CI makes optimization regression-ready. JSON output can drive CI thresholds, every result contains architecture proof, and the same pipeline can expand to larger ONNX models, more Arm cloud runners, and additional quantization strategies.",
"ArmBench CI is submitted to the Cloud AI track with public source, reproducible setup, two successful native Arm64 runs, and benchmark artifacts judges can inspect. Thank you for reviewing the project."
]
(OUT/"narration.json").write_text(json.dumps(narration,indent=2),encoding="utf-8")
print(OUT)

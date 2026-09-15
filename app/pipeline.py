from pathlib import Path
import csv, json, re, subprocess, sys, tempfile, shutil
from urllib.parse import urlparse, parse_qs

from .downloader import download_video
from .transcribe import transcribe
from .scorer import generate_candidates
from .render import render_clip
from .titles import make_title

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

def process_youtube(url: str, clip_count: int = 10):
    job_dir = Path(tempfile.mkdtemp(prefix="clipforge_", dir=str(OUTPUTS)))
    source = job_dir / "source.mp4"

    download_video(url, source)
    transcript = transcribe(source)
    candidates = generate_candidates(transcript, max_clips=clip_count)

    clips = []
    for idx, c in enumerate(candidates, 1):
        out = job_dir / f"clip_{idx:02d}.mp4"
        render_clip(source, out, c["start"], c["end"], c["text"])
        clips.append({
            "path": str(out),
            "start": c["start"],
            "end": c["end"],
            "text": c["text"],
            "score": c["score"],
            "title": make_title(c["text"]),
        })

    (job_dir / "transcript.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    return {"job_dir": str(job_dir), "clips": clips}
from pathlib import Path
import subprocess, tempfile, html

def _ass_escape(s):
    return s.replace("\\","\\\\").replace("{","\\{").replace("}","\\}")

def render_clip(source, output, start, end, text):
    duration = max(1, end-start)
    tmp = Path(tempfile.mkstemp(suffix=".ass")[1])
    safe = _ass_escape(text)
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,2,70,70,240,1

[Events]
Format: Layer, Start, End, Style, Text
Dialogue: 0,0:00:00.00,0:59:59.00,Default,{safe}
"""
    tmp.write_text(ass, encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)

    # Centre-crop to 9:16, with captions.
    vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,ass='{tmp.as_posix()}'"
    cmd = [
        "ffmpeg","-y","-ss",str(start),"-i",str(source),"-t",str(duration),
        "-vf",vf,"-c:v","libx264","-preset","veryfast","-crf","23",
        "-c:a","aac","-b:a","128k",str(output)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    tmp.unlink(missing_ok=True)
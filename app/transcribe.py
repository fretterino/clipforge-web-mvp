from faster_whisper import WhisperModel

_MODEL = None

def _model():
    global _MODEL
    if _MODEL is None:
        _MODEL = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _MODEL

def transcribe(video_path):
    model = _model()
    segments, info = model.transcribe(str(video_path), vad_filter=True, word_timestamps=False)
    out = []
    for s in segments:
        text = s.text.strip()
        if text:
            out.append({"start": float(s.start), "end": float(s.end), "text": text})
    return out
import re

HOOK_WORDS = {
    "how","why","secret","mistake","truth","never","always","money","business",
    "learn","important","problem","wrong","best","worst","actually","because",
    "lesson","advice","failure","success","controversial","nobody","everyone"
}

def _score(text):
    words = re.findall(r"\b[\w'-]+\b", text.lower())
    if not words: return 0
    hook = sum(w in HOOK_WORDS for w in words) * 4
    length = min(len(words), 35)
    punch = 8 if "?" in text or "!" in text else 0
    return min(100, 35 + hook + length + punch)

def generate_candidates(segments, max_clips=10):
    candidates = []
    n = len(segments)
    for i in range(n):
        start = segments[i]["start"]
        text_parts = []
        end = start
        for j in range(i, min(n, i+6)):
            text_parts.append(segments[j]["text"])
            end = segments[j]["end"]
            dur = end - start
            if 22 <= dur <= 58:
                text = " ".join(text_parts).strip()
                candidates.append({"start":start, "end":end, "text":text, "score":_score(text)})
                break
            if dur > 58:
                break
    # diversity by start time
    candidates.sort(key=lambda x:x["score"], reverse=True)
    chosen=[]
    for c in candidates:
        if all(abs(c["start"]-x["start"]) > 35 for x in chosen):
            chosen.append(c)
        if len(chosen) >= max_clips:
            break
    return chosen
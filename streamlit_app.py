import streamlit as st
from pathlib import Path
import tempfile, json, traceback, os, re, shutil

from app.pipeline import process_youtube

st.set_page_config(
    page_title="ClipForge",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.block-container {max-width: 760px; padding-top: 2rem; padding-bottom: 4rem;}
h1 {font-size: 2.5rem !important; letter-spacing: -0.04em;}
.small {color:#777; font-size:.9rem;}
.card {padding:1rem; border:1px solid rgba(128,128,128,.25); border-radius:16px; margin-bottom:1rem;}
.badge {display:inline-block; padding:.25rem .55rem; border-radius:999px; background:rgba(128,128,128,.15); font-size:.8rem;}
</style>
""", unsafe_allow_html=True)

if "job" not in st.session_state:
    st.session_state.job = None

st.title("✂️ ClipForge")
st.caption("Turn one long-form video into short-form clips.")

with st.container(border=True):
    st.subheader("1. Add your video")
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )
    rights = st.checkbox("I own this video or have permission/licence to repurpose it.")
    clip_count = st.slider("Number of clips", 3, 10, 10)

    if st.button("Generate clips", type="primary", use_container_width=True):
        if not url.strip():
            st.error("Paste a YouTube URL first.")
        elif not rights:
            st.error("Please confirm you have the right to repurpose the video.")
        else:
            st.session_state.job = {"status":"running"}
            with st.status("Building your clips…", expanded=True) as status:
                try:
                    result = process_youtube(url.strip(), clip_count=clip_count)
                    st.session_state.job = {"status":"done", "result":result}
                    status.update(label="Clips ready", state="complete", expanded=False)
                except Exception as e:
                    st.session_state.job = {"status":"error", "error":str(e), "trace":traceback.format_exc()}
                    status.update(label="Something went wrong", state="error", expanded=True)
                    st.exception(e)

job = st.session_state.job
if job and job.get("status") == "done":
    result = job["result"]
    st.divider()
    st.subheader(f"2. Review {len(result['clips'])} clips")
    st.caption("These are candidate clips. Approve the strongest ones for your client workflow.")

    approved = 0
    for i, clip in enumerate(result["clips"], 1):
        path = Path(clip["path"])
        with st.container(border=True):
            st.markdown(f"**Clip {i} — score {clip['score']:.0f}/100**")
            st.video(str(path))
            st.write(f"**Suggested title:** {clip['title']}")
            st.caption(f"{clip['start']:.1f}s → {clip['end']:.1f}s")
            c1, c2 = st.columns(2)
            if c1.button("✓ Approve", key=f"approve_{i}", use_container_width=True):
                st.session_state[f"approved_{i}"] = True
            if c2.button("× Skip", key=f"skip_{i}", use_container_width=True):
                st.session_state[f"approved_{i}"] = False
            if st.session_state.get(f"approved_{i}") is True:
                approved += 1

    st.success(f"{approved} clip(s) approved in this review session.")
    st.info("Next build stage: client approval dashboard + publishing connectors for YouTube Shorts and TikTok.")
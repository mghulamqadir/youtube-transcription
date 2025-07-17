import streamlit as st
import requests
import random
import time
from youtube_transcript_api import YouTubeTranscriptApi

from html_table import (
    HTML_TABLE,
)

PROXIES = HTML_TABLE

if not PROXIES:
    raise RuntimeError("No proxies found in HTML_TABLE!")


def get_random_proxy():
    return random.choice(PROXIES)

st.set_page_config(page_title="🎬 YouTube Transcript Animator", layout="centered")
st.title("🎥 YouTube Transcript Animator")

video_id = st.text_input("YouTube Video ID", value="9_Z_50I3RJs")
speed = st.sidebar.slider("Typing speed (ms per character)", 1, 50, 5)

if st.button("📜 Fetch & Animate"):
    if not video_id.strip():
        st.error("Please enter a valid Video ID.")
        st.stop()

    with st.spinner("Fetching transcript…"):
        original_get = requests.get

        def proxy_get(*args, **kwargs):
            kwargs["proxies"] = get_random_proxy()
            return original_get(*args, **kwargs)

        requests.get = proxy_get

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id.strip())
            full_text = " ".join([entry["text"] for entry in transcript])
        except Exception as e:
            st.error(f"❌ Failed to fetch transcript:\n{e}")
            st.stop()
        finally:
            requests.get = original_get

    st.success("✅ Transcript loaded! Animating now…")

    placeholder = st.empty()
    animated = ""
    for ch in full_text:
        animated += ch
        placeholder.markdown(
            f"<div style='white-space: pre-wrap; word-wrap: break-word; font-size: 1.1rem;'>{animated}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(speed / 1000.0)

    st.balloons()
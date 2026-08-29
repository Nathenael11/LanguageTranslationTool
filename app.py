# Author: Nathenael Ermias
# Language Translation Tool — CodeAlpha Internship Project
# Uses Google Cloud Translation API v2 for translation and gTTS for text-to-speech

import io
import base64

import requests
import streamlit as st
from gtts import gTTS

# ─── Language config ─────────────────────────────────────────────────────────

LANGUAGES = {
    "Afrikaans":            "af",
    "Arabic":               "ar",
    "Bengali":              "bn",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)":"zh-TW",
    "Dutch":                "nl",
    "English":              "en",
    "French":               "fr",
    "German":               "de",
    "Greek":                "el",
    "Hindi":                "hi",
    "Indonesian":           "id",
    "Italian":              "it",
    "Japanese":             "ja",
    "Korean":               "ko",
    "Malay":                "ms",
    "Persian":              "fa",
    "Polish":               "pl",
    "Portuguese":           "pt",
    "Romanian":             "ro",
    "Russian":              "ru",
    "Spanish":              "es",
    "Swahili":              "sw",
    "Swedish":              "sv",
    "Tamil":                "ta",
    "Thai":                 "th",
    "Turkish":              "tr",
    "Ukrainian":            "uk",
    "Urdu":                 "ur",
    "Vietnamese":           "vi",
}

LANGUAGE_NAMES = list(LANGUAGES.keys())

# Languages supported by gTTS for audio playback
GTTS_SUPPORTED = {
    "af", "ar", "bn", "zh-CN", "zh-TW", "nl", "en", "fr", "de", "el",
    "hi", "id", "it", "ja", "ko", "ms", "pl", "pt", "ro", "ru", "es",
    "sw", "sv", "ta", "th", "tr", "uk", "vi",
}

# Google Cloud Translation API v2 endpoint
GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_DETECT_URL    = "https://translation.googleapis.com/language/translate/v2/detect"


# ─── Helper functions ─────────────────────────────────────────────────────────

def get_api_key() -> str:
    """
    Read the Google Cloud Translation API key from Streamlit secrets.
    Works both locally (via .streamlit/secrets.toml) and on Streamlit Cloud
    (via the Secrets panel in the app settings dashboard).
    """
    try:
        return st.secrets["GOOGLE_TRANSLATE_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "❌ API key not found. Add `GOOGLE_TRANSLATE_API_KEY` to your "
            "Streamlit secrets (`.streamlit/secrets.toml` locally, or the "
            "Secrets panel on Streamlit Community Cloud)."
        )
        st.stop()


def translate_text(text: str, source_lang: str, target_lang: str, api_key: str) -> str:
    """
    Translate *text* from source_lang to target_lang using the
    Google Cloud Translation REST API v2 (Basic tier).

    Returns the translated string.
    Raises requests.HTTPError on a non-2xx response.
    """
    params = {
        "q":      text,
        "source": source_lang,
        "target": target_lang,
        "format": "text",
        "key":    api_key,
    }
    resp = requests.post(GOOGLE_TRANSLATE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["translations"][0]["translatedText"]


def generate_audio(text: str, lang_code: str) -> bytes:
    """
    Generate MP3 audio for *text* in *lang_code* using gTTS.
    Returns raw MP3 bytes (no temp files written to disk).
    """
    tts = gTTS(text=text, lang=lang_code, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def audio_to_data_uri(mp3_bytes: bytes) -> str:
    """Encode MP3 bytes as a base64 data URI for inline HTML playback."""
    b64 = base64.b64encode(mp3_bytes).decode("utf-8")
    return f"data:audio/mpeg;base64,{b64}"


# ─── Page setup ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered",
)

st.title("🌐 Language Translation Tool")
st.markdown("*Built by Nathenael Ermias*")
st.markdown("Powered by **Google Cloud Translation API v2**")
st.markdown("---")

# ─── Language selectors ───────────────────────────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    source_name = st.selectbox(
        "Source language",
        LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index("English"),
    )

with col2:
    target_name = st.selectbox(
        "Target language",
        LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index("Spanish"),
    )

source_code = LANGUAGES[source_name]
target_code = LANGUAGES[target_name]

# ─── Text input ───────────────────────────────────────────────────────────────

input_text = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste your text here…",
)

translate_btn = st.button("🌐 Translate", type="primary", use_container_width=True)

st.markdown("---")

# ─── Translation ──────────────────────────────────────────────────────────────

if translate_btn:
    if not input_text or not input_text.strip():
        st.warning("⚠️ Please enter some text before clicking Translate.")

    elif source_code == target_code:
        st.info("ℹ️ Source and target languages are the same — nothing to translate.")

    else:
        api_key = get_api_key()
        with st.spinner("Sending request to Google Cloud Translation API…"):
            try:
                translated = translate_text(
                    input_text.strip(), source_code, target_code, api_key
                )
                st.session_state["translated"]   = translated
                st.session_state["target_code"]  = target_code
                st.session_state["target_name"]  = target_name
            except requests.HTTPError as e:
                status = e.response.status_code if e.response is not None else "unknown"
                st.error(
                    f"❌ Google Translate API returned HTTP {status}. "
                    f"Check that your API key is valid and the Cloud Translation API "
                    f"is enabled in your Google Cloud project.\n\nDetail: {e}"
                )
                st.session_state.pop("translated", None)
            except requests.ConnectionError:
                st.error("❌ Network error — could not reach the Google Translate API. Check your internet connection.")
                st.session_state.pop("translated", None)
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
                st.session_state.pop("translated", None)

# ─── Display result ───────────────────────────────────────────────────────────

if "translated" in st.session_state and st.session_state["translated"]:
    translated_text = st.session_state["translated"]
    result_lang     = st.session_state.get("target_name", "")
    result_code     = st.session_state.get("target_code", "en")

    st.subheader(f"✅ Translation ({result_lang})")

    # Read-only output box
    st.text_area(
        label="translated_output",
        value=translated_text,
        height=150,
        key="result_box",
        label_visibility="collapsed",
    )

    # ── Copy to clipboard ──────────────────────────────────────────────────
    safe_text = translated_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    copy_js = f"""
    <script>
    function copyTranslation() {{
        const text = `{safe_text}`;
        navigator.clipboard.writeText(text).then(function() {{
            const btn = document.getElementById('copy-btn');
            btn.innerText = '✅ Copied!';
            btn.style.background = '#388E3C';
            setTimeout(() => {{
                btn.innerText = '📋 Copy to clipboard';
                btn.style.background = '#4CAF50';
            }}, 2000);
        }}, function(err) {{
            alert('Could not copy: ' + err);
        }});
    }}
    </script>
    <button id="copy-btn"
        onclick="copyTranslation()"
        style="background:#4CAF50;color:white;border:none;padding:9px 20px;
               border-radius:6px;cursor:pointer;font-size:14px;font-weight:500;
               transition:background 0.2s;">
        📋 Copy to clipboard
    </button>
    """
    st.components.v1.html(copy_js, height=55)

    # ── Text-to-speech ────────────────────────────────────────────────────
    if result_code in GTTS_SUPPORTED:
        if st.button("🔊 Play translation (text-to-speech)", use_container_width=False):
            with st.spinner("Generating audio…"):
                try:
                    mp3_bytes = generate_audio(translated_text, result_code)
                    data_uri  = audio_to_data_uri(mp3_bytes)
                    st.components.v1.html(
                        f"""<audio controls autoplay style="width:100%;margin-top:6px;">
                                <source src="{data_uri}" type="audio/mpeg">
                            </audio>""",
                        height=60,
                    )
                except Exception as e:
                    st.error(f"❌ Audio generation failed: {e}")
    else:
        st.caption(f"ℹ️ Text-to-speech is not available for {result_lang}.")

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "Translation: [Google Cloud Translation API v2](https://cloud.google.com/translate/docs/basic/translating-text) · "
    "TTS: [gTTS](https://github.com/pndurette/gTTS) · "
    "Built by Nathenael Ermias"
)

# Author: Nathenael Ermias
# Language Translation Tool — CodeAlpha Internship Project
# Uses deep-translator (Google Translate API wrapper) for translation
# and gTTS for text-to-speech playback.

import io
import base64

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

# ─── Language config ─────────────────────────────────────────────────────────

LANGUAGES = {
    "Afrikaans":             "af",
    "Arabic":                "ar",
    "Bengali":               "bn",
    "Chinese (Simplified)":  "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Dutch":                 "nl",
    "English":               "en",
    "French":                "fr",
    "German":                "de",
    "Greek":                 "el",
    "Hindi":                 "hi",
    "Indonesian":            "id",
    "Italian":               "it",
    "Japanese":              "ja",
    "Korean":                "ko",
    "Malay":                 "ms",
    "Persian":               "fa",
    "Polish":                "pl",
    "Portuguese":            "pt",
    "Romanian":              "ro",
    "Russian":               "ru",
    "Spanish":               "es",
    "Swahili":               "sw",
    "Swedish":               "sv",
    "Tamil":                 "ta",
    "Thai":                  "th",
    "Turkish":               "tr",
    "Ukrainian":             "uk",
    "Urdu":                  "ur",
    "Vietnamese":            "vi",
}

LANGUAGE_NAMES = list(LANGUAGES.keys())

# Languages supported by gTTS for audio playback
GTTS_SUPPORTED = {
    "af", "ar", "bn", "zh-CN", "zh-TW", "nl", "en", "fr", "de", "el",
    "hi", "id", "it", "ja", "ko", "ms", "pl", "pt", "ro", "ru", "es",
    "sw", "sv", "ta", "th", "tr", "uk", "vi",
}


# ─── Translation & TTS helpers ────────────────────────────────────────────────

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate *text* from source_lang to target_lang via the
    Google Translate API (accessed through deep-translator's GoogleTranslator).

    Returns the translated string.
    Raises an exception on network or API failure — handled in the UI layer.
    """
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)


def generate_audio(text: str, lang_code: str) -> bytes:
    """
    Generate MP3 audio bytes for *text* using gTTS.
    No temp files are written to disk — audio is returned as raw bytes.
    """
    tts = gTTS(text=text, lang=lang_code, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def audio_to_data_uri(mp3_bytes: bytes) -> str:
    """Encode raw MP3 bytes as a base64 data URI for inline browser playback."""
    b64 = base64.b64encode(mp3_bytes).decode("utf-8")
    return f"data:audio/mpeg;base64,{b64}"


# ─── Page setup ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered",
)

st.title("🌐 Language Translation Tool")
st.markdown("*Built by Nathenael Ermias*")
st.markdown("Powered by **Google Translate API** via deep-translator")
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

# ─── Translation logic ────────────────────────────────────────────────────────

if translate_btn:
    if not input_text or not input_text.strip():
        st.warning("⚠️ Please enter some text before clicking Translate.")

    elif source_code == target_code:
        st.info("ℹ️ Source and target languages are the same — nothing to translate.")

    else:
        with st.spinner("Sending text to Google Translate API…"):
            try:
                translated = translate_text(input_text.strip(), source_code, target_code)
                st.session_state["translated"]  = translated
                st.session_state["target_code"] = target_code
                st.session_state["target_name"] = target_name
            except Exception as e:
                st.error(
                    f"❌ Translation failed. This is usually a network issue or an "
                    f"unsupported language pair.\n\nError detail: {e}"
                )
                st.session_state.pop("translated", None)

# ─── Display result ───────────────────────────────────────────────────────────

if "translated" in st.session_state and st.session_state["translated"]:
    translated_text = st.session_state["translated"]
    result_lang     = st.session_state.get("target_name", "")
    result_code     = st.session_state.get("target_code", "en")

    st.subheader(f"✅ Translation ({result_lang})")

    # Read-only output text area
    st.text_area(
        label="translated_output",
        value=translated_text,
        height=150,
        key="result_box",
        label_visibility="collapsed",
    )

    # ── Copy to clipboard ─────────────────────────────────────────────────
    safe_text = translated_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    copy_js = f"""
    <script>
    function copyTranslation() {{
        const text = `{safe_text}`;
        navigator.clipboard.writeText(text).then(function() {{
            const btn = document.getElementById('copy-btn');
            btn.innerText = '\u2705 Copied!';
            btn.style.background = '#388E3C';
            setTimeout(() => {{
                btn.innerText = '\U0001f4cb Copy to clipboard';
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
               border-radius:6px;cursor:pointer;font-size:14px;font-weight:500;">
        \U0001f4cb Copy to clipboard
    </button>
    """
    st.components.v1.html(copy_js, height=55)

    # ── Text-to-speech playback ───────────────────────────────────────────
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
    "Translation: [Google Translate API](https://cloud.google.com/translate) "
    "via [deep-translator](https://github.com/nidhaloff/deep-translator) · "
    "TTS: [gTTS](https://github.com/pndurette/gTTS) · "
    "Built by Nathenael Ermias"
)

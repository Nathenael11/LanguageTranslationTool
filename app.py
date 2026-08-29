# Author: Nathenael Ermias
# Language Translation Tool — CodeAlpha Internship Project
# Uses deep-translator (Google Translate wrapper) and gTTS for text-to-speech

import io
import base64
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

# ─── Language config ────────────────────────────────────────────────────────────

LANGUAGES = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Dutch": "nl",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hindi": "hi",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Malay": "ms",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
}

LANGUAGE_NAMES = list(LANGUAGES.keys())

# Languages supported by gTTS (subset of above)
GTTS_SUPPORTED = {
    "af", "ar", "bn", "zh-CN", "zh-TW", "nl", "en", "fr", "de", "el",
    "hi", "id", "it", "ja", "ko", "ms", "pl", "pt", "ro", "ru", "es",
    "sw", "sv", "ta", "th", "tr", "uk", "vi",
}


# ─── Helper functions ────────────────────────────────────────────────────────────

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text using deep-translator's GoogleTranslator.
    source_lang / target_lang are BCP-47 codes (e.g. "en", "fr").
    Returns the translated string or raises an exception on failure.
    """
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)


def generate_audio(text: str, lang_code: str) -> bytes:
    """
    Generate MP3 audio bytes for the given text using gTTS.
    Returns raw MP3 bytes.
    """
    tts = gTTS(text=text, lang=lang_code, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def audio_to_data_uri(mp3_bytes: bytes) -> str:
    """Encode MP3 bytes as a data URI for inline HTML playback."""
    b64 = base64.b64encode(mp3_bytes).decode("utf-8")
    return f"data:audio/mpeg;base64,{b64}"


# ─── Page setup ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered",
)

st.title("🌐 Language Translation Tool")
st.markdown("*Built by Nathenael Ermias*")
st.markdown("---")

# ─── UI inputs ──────────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    source_name = st.selectbox(
        "Source language",
        LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index("English"),
    )

with col2:
    default_target = "Spanish"
    target_name = st.selectbox(
        "Target language",
        LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index(default_target),
    )

source_code = LANGUAGES[source_name]
target_code = LANGUAGES[target_name]

input_text = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste your text here…",
)

translate_btn = st.button("Translate", type="primary", use_container_width=True)

st.markdown("---")

# ─── Translation logic ───────────────────────────────────────────────────────────

if translate_btn:
    # Validate input
    if not input_text or not input_text.strip():
        st.warning("Please enter some text before clicking Translate.")
    elif source_code == target_code:
        st.info("Source and target languages are the same — nothing to translate.")
    else:
        with st.spinner("Translating…"):
            try:
                translated = translate_text(input_text.strip(), source_code, target_code)
                st.session_state["translated"] = translated
                st.session_state["target_code"] = target_code
                st.session_state["target_name"] = target_name
            except Exception as e:
                st.error(
                    f"Translation failed. This can happen if the language pair is unsupported "
                    f"or if there is a network issue.\n\nError detail: {e}"
                )
                st.session_state.pop("translated", None)

# ─── Display result ──────────────────────────────────────────────────────────────

if "translated" in st.session_state and st.session_state["translated"]:
    translated_text = st.session_state["translated"]
    result_lang = st.session_state.get("target_name", "")
    result_code = st.session_state.get("target_code", "en")

    st.subheader(f"Translation ({result_lang})")
    st.text_area(
        label="Translated text",
        value=translated_text,
        height=150,
        key="result_box",
        label_visibility="collapsed",
    )

    # Copy-to-clipboard button via JavaScript injection
    copy_js = f"""
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText({translated_text!r}).then(function() {{
            document.getElementById('copy-btn').innerText = '✅ Copied!';
            setTimeout(() => document.getElementById('copy-btn').innerText = '📋 Copy to clipboard', 2000);
        }}, function(err) {{
            alert('Could not copy text: ' + err);
        }});
    }}
    </script>
    <button id="copy-btn"
        onclick="copyToClipboard()"
        style="
            background:#4CAF50; color:white; border:none; padding:8px 18px;
            border-radius:6px; cursor:pointer; font-size:14px; margin-right:8px;">
        📋 Copy to clipboard
    </button>
    """
    st.components.v1.html(copy_js, height=50)

    # Text-to-speech playback
    if result_code in GTTS_SUPPORTED:
        tts_btn = st.button("🔊 Play translation (TTS)", use_container_width=False)
        if tts_btn:
            with st.spinner("Generating audio…"):
                try:
                    mp3_bytes = generate_audio(translated_text, result_code)
                    data_uri = audio_to_data_uri(mp3_bytes)
                    audio_html = f"""
                    <audio controls autoplay style="width:100%; margin-top:8px;">
                        <source src="{data_uri}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                    """
                    st.components.v1.html(audio_html, height=60)
                except Exception as e:
                    st.error(
                        f"Audio generation failed. This can happen if the language is not "
                        f"supported by the TTS engine or if there is a network issue.\n\nError: {e}"
                    )
    else:
        st.caption(f"ℹ️ Text-to-speech is not available for {result_lang}.")

# ─── Footer ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "Powered by [deep-translator](https://github.com/nidhaloff/deep-translator) "
    "& [gTTS](https://github.com/pndurette/gTTS) · "
    "Built by Nathenael Ermias"
)

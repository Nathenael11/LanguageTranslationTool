# Language Translation Tool

**GitHub:** https://github.com/Nathenael11/LanguageTranslationTool

**Live demo:** *(link will be added after deployment)*

Built by Nathenael Ermias

---

## What this is

A web app that lets you translate text between 30 of the most common world languages using the **Google Cloud Translation API v2**. You type text, choose a source and target language, click Translate, and the result appears on screen. You can also copy the result to clipboard or hear it read aloud using text-to-speech.

Built as part of the CodeAlpha internship.

---

## How to run it locally

**Requirements:** Python 3.9 or higher, a Google Cloud Translation API key.

1. Clone the repo:

```bash
git clone https://github.com/Nathenael11/LanguageTranslationTool.git
cd LanguageTranslationTool
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API key to `.streamlit/secrets.toml`:

```toml
GOOGLE_TRANSLATE_API_KEY = "your-api-key-here"
```

5. Run the app:

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Project structure

```
LanguageTranslationTool/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies (pinned versions)
├── README.md               # This file
├── .streamlit/
│   ├── config.toml         # Streamlit theme settings
│   └── secrets.toml        # API key (local only, not committed)
└── .gitignore
```

---

## How the translation works

The app sends a POST request to the **Google Cloud Translation API v2** (`translation.googleapis.com/language/translate/v2`) with:
- The input text
- The source language code (e.g. `en`)
- The target language code (e.g. `fr`)
- Your API key

The API returns the translated text, which is displayed on screen. This is the official Google Cloud Translation Basic tier — the same technology behind Google Translate.

To use it, you need to:
1. Enable the **Cloud Translation API** in your Google Cloud project
2. Generate an **API key** in Google Cloud Console → APIs & Services → Credentials
3. Add the key to `.streamlit/secrets.toml` locally or to the Secrets panel on Streamlit Community Cloud

---

## How text-to-speech works

After a translation is done, you can click "Play translation (text-to-speech)" to hear the result read aloud. This uses [gTTS (Google Text-to-Speech)](https://github.com/pndurette/gTTS), which generates an MP3 in memory and plays it directly in the browser without saving any files to disk.

Not all 30 languages are supported by gTTS. If the target language has no TTS support, a notice is shown instead of the play button.

---

## Supported languages (30 total)

Afrikaans, Arabic, Bengali, Chinese (Simplified), Chinese (Traditional), Dutch, English, French, German, Greek, Hindi, Indonesian, Italian, Japanese, Korean, Malay, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Swahili, Swedish, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese.

---

## Example translations

| Input text | Source | Target | Output |
|---|---|---|---|
| Hello, how are you? | English | Spanish | Hola, ¿cómo estás? |
| I love programming. | English | French | J'aime la programmation. |
| Good morning | English | Japanese | おはようございます |
| Thank you very much | English | Arabic | شكرا جزيلا |
| Where is the library? | English | German | Wo ist die Bibliothek? |

---

## Error handling

- Empty input → warning message, no API call made
- Same source and target language → info message, no API call made
- API key missing or invalid → clear error message with instructions
- Network failure → error message with description
- TTS failure → error message, app does not crash

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | 1.62.0 | Web UI framework |
| requests | 2.34.2 | HTTP calls to Google Cloud Translation API |
| gTTS | 2.5.4 | Text-to-speech audio generation |

---

Built by Nathenael Ermias — CodeAlpha Internship Project

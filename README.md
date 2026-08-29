# Language Translation Tool

**GitHub:** https://github.com/Nathenael11/LanguageTranslationTool

**Live demo:** https://languagetranslationtool-zki9hewgtnzxc7hnindfqt.streamlit.app

Built by Nathenael Ermias

---

## What this is

A web app that translates text between 30 of the most common world languages using the **Google Translate API** (via the deep-translator library). You type text, pick source and target languages, click Translate, and the result appears on screen. You can also copy the result to clipboard or hear it read aloud with text-to-speech.

Built as part of the CodeAlpha internship.

---

## How to run it locally

**Requirements:** Python 3.9 or higher.

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

4. Run the app:

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Project structure

```
LanguageTranslationTool/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies (pinned versions)
├── README.md           # This file
├── .streamlit/
│   └── config.toml     # Streamlit theme settings
└── .gitignore
```

---

## How the translation works

Translation is done using [deep-translator](https://github.com/nidhaloff/deep-translator), which sends text to the **Google Translate API** and returns the translated result. No API key or billing account is required — deep-translator uses the same public endpoint that powers Google Translate.

The app supports 30 languages including English, Spanish, French, German, Chinese (Simplified and Traditional), Arabic, Hindi, Japanese, Korean, Russian, Portuguese, Italian, and more.

---

## How text-to-speech works

After a translation is produced, you can click "Play translation (text-to-speech)" to hear the text read aloud. This uses [gTTS (Google Text-to-Speech)](https://github.com/pndurette/gTTS), which generates an MP3 in memory and plays it directly in the browser. No temp files are saved to disk.

Not all 30 languages are supported by gTTS. If the target language doesn't support TTS, a notice is shown instead of the play button.

---

## Supported languages (31 total)

Afrikaans, Amharic, Arabic, Bengali, Chinese (Simplified), Chinese (Traditional), Dutch, English, French, German, Greek, Hindi, Indonesian, Italian, Japanese, Korean, Malay, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Swahili, Swedish, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese.

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
- Network or API failure → error message with detail, app does not crash
- TTS failure → error message shown, rest of the app keeps working

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | 1.62.0 | Web UI framework |
| deep-translator | 1.11.4 | Google Translate API wrapper |
| gTTS | 2.5.4 | Text-to-speech audio generation |

---

Built by Nathenael Ermias — CodeAlpha Internship Project

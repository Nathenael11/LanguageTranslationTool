# Language Translation Tool

**Live demo:** *(link will be added after deployment)*

Built by Nathenael Ermias

---

## What this is

A simple web app that lets you translate text between 30 of the most common world languages. You type something in, pick a source and target language, hit Translate, and the result appears on screen. You can also copy the result to your clipboard or play it back as audio using text-to-speech.

This was built as part of the CodeAlpha internship.

---

## How to run it locally

**Requirements:** Python 3.9 or higher.

1. Clone the repo:

```bash
git clone https://github.com/Nathenael11/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
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
CodeAlpha_LanguageTranslationTool/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies (pinned versions)
├── README.md           # This file
├── .streamlit/
│   └── config.toml     # Streamlit theme settings
└── .gitignore
```

---

## How the translation works

Translation is done using the [deep-translator](https://github.com/nidhaloff/deep-translator) library, specifically its `GoogleTranslator` class. This wraps Google Translate's web interface without needing an API key. The library sends your text to Google's translation endpoint and returns the result.

The app supports 30 languages including English, Spanish, French, German, Chinese (Simplified and Traditional), Arabic, Hindi, Japanese, Korean, Russian, Portuguese, Italian, and more.

---

## How text-to-speech works

After a translation is produced, you can click "Play translation (TTS)" to hear the translated text read aloud. This uses [gTTS (Google Text-to-Speech)](https://github.com/pndurette/gTTS), a Python library that generates an MP3 from text. The audio is generated on the fly and played in the browser without saving any files to disk.

Not all languages are supported by gTTS — if a language doesn't support TTS, a notice is shown instead of the play button.

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

- If you click Translate without entering text, a warning message appears.
- If the source and target language are the same, an info message appears.
- If the translation fails (network issue, unsupported pair, etc.), an error message is shown with details — the app does not crash.
- If TTS fails, an error message is shown and the audio is not played.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | 1.39.0 | Web UI framework |
| deep-translator | 1.11.4 | Translation (Google Translate wrapper) |
| gTTS | 2.5.1 | Text-to-speech audio generation |

---

Built by Nathenael Ermias — CodeAlpha Internship Project

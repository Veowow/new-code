from __future__ import annotations


def translate_batch(texts: list[str], target_lang: str, source_lang: str = "auto") -> list[str]:
    try:
        from deep_translator import GoogleTranslator

        src = "auto" if source_lang == "auto" else source_lang
        translator = GoogleTranslator(source=src, target=target_lang)
        return [translator.translate(t) for t in texts]
    except Exception:
        return [f"[译]{t}" for t in texts]

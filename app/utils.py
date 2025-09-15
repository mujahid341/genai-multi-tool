import logging
from datetime import datetime

def detect_intent(query: str, override: str):
    q = query.lower()
    if override != "Auto":
        return override.lower()
    if "translate" in q or "in hindi" in q or "to spanish" in q:
        return "translate"
    if "code" in q or "script" in q or "function" in q:
        return "code"
    if "summarize" in q or "summary" in q:
        return "summarize"
    return "text"

def log_event(query, intent, lang, error=None):
    log_format = f"{datetime.now()} | Mode: {intent} | Lang: {lang} | Query: {query}"
    if error:
        log_format += f" | ERROR: {error}"
    with open("logs/assistant.log", "a") as f:
        f.write(log_format + "\n")

def save_output(result):
    with open("logs/last_output.txt", "w", encoding="utf-8") as f:
        f.write(result)

def build_prompt(user_input, intent, lang_output):
    if intent == "code":
        return f"Write clean, commented code for this request:\n\n{user_input}"
    elif intent == "translate":
        return f"Translate this to {lang_output}:\n\n{user_input}"
    elif intent == "summarize":
        return f"Summarize the following content:\n\n{user_input}"
    else:
        return f"Generate text based on this prompt:\n\n{user_input}"

import re
from constants import replacements, bad_words

def preprocess_message(message):
    for original, pattern in replacements.items():
        message = re.sub(pattern, original, message, flags=re.IGNORECASE)

    return message

def check_message(message):
    message_lower = message.lower()

    processed_message = preprocess_message(message_lower)
    print(processed_message)

    for word in bad_words:
        pattern = r'\b' + re.escape(word)
        if re.search(pattern, processed_message):
            return True
    return False


if __name__ == '__main__':
    print(check_message("С᧘ᥙᴛыᥱ ɯκуρы"))
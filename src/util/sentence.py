import re

current_sentence = ""
def to_sentence(token: str):
        global current_sentence
        for char in token:
            if re.match(r"[,.\?!，。？！\n\r\t]", char):
                current_sentence += char
                if current_sentence.strip():
                    current_sentence = ""
            else:
                current_sentence += char
import re

def get_clean_word(word):
    cleaned_word = re.sub(r"[^א-ת'ؠ-يٱ-ٳٶ-ە]", "", word)
    return cleaned_word

def get_sound_index(word):

    sound_index = ""
    letters = word
    dbl = False
    # Removes chars which aren't Hebrew or Arabic letters, or Geresh
    letters = re.sub(r"[^א-ת'ؠ-يٱ-ٳٶ-ە]", "", letters)

    for character_index, character in enumerate(letters):
        next_char = character_index + 1
        if dbl:
            dbl = False
        elif character in ["א", "ו", "י"]:
            if character_index > 0:
                sound_index += "" # hebrew a'he'vi
            else:
                if character in ["א"]:
                    sound_index += "A"
                elif character in ["ו"]:
                    sound_index += "W"
                else:
                    sound_index += "Y"
        elif character in ["צ", "ץ", "ד"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "D"
            dbl = True
        elif character in ["ט"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "S"
            dbl = True
        elif character in ["ת"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "T"
            dbl = True
        elif character in ["ה", "ח"] and next_char < len(word) and word[character_index +1] == "'":
            sound_index += "H"
            dbl = True
        elif character in ["ג", "ז"] and next_char < len(word) and word[character_index + 1] == "'":
            sound_index += "J"
            dbl = True
        elif character in ["ר"] and next_char < len(word) and word[character_index + 1] == "'":
            sound_index += "R"
            dbl = True
        # arabic letters
        elif character in ["ا", "آ", "أ", "إ", "ئ", "ة", "ء", "ؤ", "ي", "ى", "و"]:
            sound_index += ""
        elif character in ["د", "ד", "ذ", "ד'", "ض", "צ'", "ץ'", ]:
            sound_index += "D"
        elif character in ["ص", "צ", "ץ", "س", "ס", "ز", "ז", "ظ", "ט'"]:
            sound_index += "S"
        elif character in ["ط", "ט", "ت", "ת", "ث", "ת'"]:
            sound_index += "T"
        elif character in ["ب", "ב"]:
            sound_index += "B"
        elif character in ["ن", "נ", "ן"]:
            sound_index += "N"
        elif character in ["ع", "ע"]:
            sound_index += "A"
        elif character in ['ة', 'ه', "ה", "ה'", "ح", "ח", "ח'", "خ"]:
            sound_index += "H"
        elif character in ["ك", "כ", "ך", "ق", "ק", "ג"]:
            sound_index += "K"
        elif character in ["ش", "ש", "ج", "ג'", "ז'"]:
            sound_index += "J"
        elif character in ["غ", "ע'", "ر", "ר", "ר'"]:  # TODO "ע'" not working
            sound_index += "R"
        elif character in ["ل", "ל"]:
            sound_index += "L"
        elif character in ["م", "מ", "ם"]:
            sound_index += "M"
        elif character in ["ف", "פ", "ף"]:
            sound_index += "F"
        else:
            sound_index += character

    return sound_index


assert get_sound_index("עיתונות") == "ATNT"
assert get_sound_index("עזר") == "ASR"
assert get_sound_index("שכל") == "JKL"
assert get_sound_index("כאפיה") == "KFH"
assert get_sound_index("החלטה") == "HHLTH"

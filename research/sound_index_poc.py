
def get_sound_index(word):

    sound_index = ""

    for character_index, character in enumerate(word):

        if character in ["צ", "ץ", "ד"] and word[character_index +1] == "'":
            sound_index += "D"
        elif character in ["ט"] and word[character_index +1] == "'":
            sound_index += "S"
        elif character in ["ת"] and word[character_index +1] == "'":
            sound_index += "T"
        elif character in ["ה", "ח"] and word[character_index +1] == "'":
            sound_index += "H"
        elif character in ["ג", "ז"] and word[character_index + 1] == "'":
            sound_index += "J"
        elif character in ["ר"] and word[character_index + 1] == "'":
            sound_index += "R"
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
        elif character in ["غ", "ע'", "ر", "ר", "ר'"]:
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


print(get_sound_index("עזר"))

#assert get_sound_index("עיתונות") == "ATNT"
# assert get_sound_index("עזר") == "ASR"
# assert get_sound_index("שכל") == "JKL"

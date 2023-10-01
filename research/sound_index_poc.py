

def get_sound_index(word):

    sound_index = ""

    for character_index, character in enumerate(word):

        if character in ["צ", "ץ", "ד"] and word[character_index+1] == "'":
            sound_index += "D"
        elif character in ["ט"] and word[character_index+1] == "'":
            sound_index += "S"
        elif character in ["ת"] and word[character_index+1] == "'":
            sound_index += "S"

    return sound_index


print(get_sound_index("עזר"))


# assert get_sound_index("עיתונות") == "ATNT"
# assert get_sound_index("עזר") == "ASR"
# assert get_sound_index("שכל") == "JKL"

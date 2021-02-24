import emoji_data_python
from emoji import unicode_codes
from emoji_extractor.extract import Extractor
import emoji
import regex
# https://www.webfx.com/tools/emoji-cheat-sheet/
#print(emoji.emojize('Python is :thumbs_up:'))
#print(emoji.emojize('Python is :lipstick:', use_aliases=True))
#print(emoji.demojize('Python is 👍'))
#print(emoji.emojize("Python is fun :red_heart:"))
#print(emoji.emojize("Python is fun :red_heart:",variant="emoji_type"))


def split_count(text):
    emoji_counter = 0
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.emoji_count for char in word):
            emoji_counter += 1
            # Remove from the given text the emojis
            text = text.replace(word, '')

    words_counter = len(text.split())

    return emoji_counter, words_counter


line = "❤️❤️❤️zcxzxczxczxc❤️❤️❤️😊❤️😊😎🤩😘🌟💵🙅🙅"
# print(len(line))
extract = Extractor()
count = extract.count_emoji(line)
print(count.most_common())


cuenta = emoji.emoji_count(line)
# print(cuenta)


cuenta = emoji_data_python.get_emoji_regex().findall(line)
print(cuenta)

#print(emoji_data_python.find_by_name("NEW MOON SYMBOL"))
a = ':Mrs._Claus_medium-light_skin_tone:'
b = ':OK_hand_medium_skin_tone:'
c = ':T-Rex:'
d = ':A_button_(blood_type):'
#print(emoji_data_python.replace_colons('Hello world ! :wave::skin-tone-3: :earth_africa: :OK_hand_medium_skin_tone: :T-Rex:'))

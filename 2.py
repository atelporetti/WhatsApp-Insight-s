import emoji
# https://www.webfx.com/tools/emoji-cheat-sheet/
print(emoji.emojize('Python is :thumbs_up:'))
print(emoji.emojize('Python is :lipstick:', use_aliases=True))
print(emoji.demojize('Python is 👍'))
print(emoji.emojize("Python is fun :red_heart:"))
print(emoji.emojize("Python is fun :red_heart:",variant="emoji_type"))
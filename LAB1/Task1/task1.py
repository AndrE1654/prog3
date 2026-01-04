def collect_words_info(text_line):
    words = text_line.lower().split()
    stats = {}

    for w in words:
        # прибираємо розділові знаки
        clean_word = w.strip(",.?!")

        if clean_word in stats:
            stats[clean_word] += 1
        else:
            stats[clean_word] = 1

    return stats

text = """
Слово, чому ти не твердая криця,
Що серед бою так ясно іскриться?
Чом ти не гострий, безжальний, як меч,
Той, що здіймає війни кривавий смерч?

Слово, моя ти єдиная зброє,
Ми не повинні загинуть обоє!
Може, в руках невідомих братів
Станеш ти кращим мечем на катів.

Слово, чому ти не криця твердая?
Чом не летиш ти стрілою крилатою?
Слово, чому ти не гострий кинджал,
Що розтинає неправди овал?
"""

result = collect_words_info(text)

more_than_three = []
for word, count in result.items():
    if count > 3:
        more_than_three.append(word)

print("Словник слів:", result)
print("Слова, що зустрічаються більше 3 разів:", more_than_three)

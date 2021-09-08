import random

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from nltk.corpus import stopwords
from string import punctuation

russian_stopwords = stopwords.words("russian")


# Получение текстовой строки из списка слов
async def str_corpus(corpus):
    string_corpus = ''
    async for i in corpus:
        string_corpus += ' ' + i
    string_corpus = string_corpus.strip()
    return string_corpus


# Получение списка всех слов в корпусе
async def get_corpus(data):
    corpus = []
    async for phrase in data:
        async for word in phrase.split():
            corpus.append(word)
    return corpus


# Получение облака слов
async def get_word_cloud(corpus):
    word_cloud = WordCloud(background_color='white',
                           stopwords=STOPWORDS,
                           width=3000,
                           height=2500,
                           max_words=200,
                           random_state=42
                           ).generate(await str_corpus(corpus))
    return word_cloud


# Удаление знаков пунктуации из текста
def remove_punct(text):
    table = {33: '', 34: '', 35: '', 36: '', 37: '', 38: '', 39: '', 40: '', 41: '', 42: '', 43: '', 44: '', 45: '',
             46: '', 47: '', 58: '', 59: '', 60: '', 61: '', 62: '', 63: '', 64: '', 91: '', 92: '', 93: '', 94: '',
             95: '', 96: '', 123: '', 124: '', 125: '', 126: '', r"\n": ''}
    return text.translate(table)


shop_string = "магазин деньги продукты покупать покупатель товар вещи продавец касса шопинг супермаркет чек пакет " \
              "тележка цена продажа кассир приобретение радость трата подарок сумка стоимость скидки оплата корзина " \
              "акция салон витрина платить базар бутик киоск сумма кошелёк обновка покупки корзинка универмаг " \
              "универсамраспродажа гипермаркет консультант aliexpress юла авито avito халява халявный"

trader_string = "торговля хомяк акционер хаях тинькофф курс tal spce биткоин биткоина bitcoin шортить котлету tsmc" \
                " ту зе мун"

humor_string = "смех шутка анекдот улыбка веселье радость смешно юморист " \
               "камеди клоун КВН комедия ржач хохот смеяться " \
               "весело сатира прикол чёрный сарказм цирк умора смешной шутник шоу комик аншлаг юрмала чувство" \
               "сцена ирония шутить счастье ржака концерт передача стендап юморной зубы жизнь аплодисменты зал радио" \
               "настроение слёзы рассказ смешить Задорнов пародия развлечение хохол хаха хохма ералаш забава " \
               "остроумие шут актёр театр артист подкол юмореска выступление воля дети плач угар язык гогот задор " \
               "скетч эмоции юморок история сатирик юморить истерика розыгрыш смешинка юмористический ТНТ" \
               "жанр стёб отдых ржать семья семье семью мужик мужики еврей евреи хохлы хохла жена женой женщина" \
               "старик старика внуки внук как называется штирлиц штирлица " \
               "официант эрнест хемингуэй котлету спрашивают" \
               " спрашивали медведь заяц волк лиса воронв гусь свинье товарищ юмор журналист трюк"

news_string = "авария трагедия новости пожар пожара" \
              " колонии колония дтп всу днр война войны ответный удар сцкк обстрел сбила " \
              "сбил сбили насмерть пенсионера пенсионерку срок срока мошенничество" \
              " разрушили разрушила разрушило разрушил " \
              "труп завоевал бронзу бронзы серебро серебра золото золота обращение росприроднадзор роскомнадзор " \
              "нарушил нарушили нарушила нарушитель правонарушитель вреда травмы травма средней тяжести город города" \
              " область области больница больницы больнице гости гостю гостям отметил заморозки убийство убийстве" \
              " убийства мэрии мэрия школ школы школа нефтезавод говорится " \
              "сообщении сообщения жители жителем автобуса " \
              "ер ук рф заболевших оон g20 covid-19 огня огнём талибы параолимпийцы место афганистан евросоюз новость " \
              "новости журналист"


async def cleanup_input(input_string):
    if input_string is not None:
        input_string = input_string.lower()
        input_array = input_string.split(" ")
        output_array = []

        for word in input_array:
            output_array.append(remove_punct(word))

        for word in output_array:
            if word not in russian_stopwords and word != " " and word.strip() not in punctuation:
                pass
            else:
                output_array.remove(word)
        return output_array
    else:
        return "магазин торговля смех авария"


def get_post_theme(input_array):
    shop_theme = shop_string.split(" ")
    trader_theme = trader_string.split(" ")
    humor_theme = humor_string.split(" ")
    news_theme = news_string.split(" ")
    post_theme = {"shopping": False, "trading": False, "humor": False, "news": False}
    for word in input_array:
        if word in shop_theme and post_theme["shopping"] is False:
            post_theme["shopping"] = True

        if word in trader_theme and post_theme["trading"] is False:
            post_theme["trading"] = True

        if word in humor_theme and post_theme["humor"] is False:
            post_theme["humor"] = True

        if word in news_theme and post_theme["news"] is False:
            post_theme["news"] = True
    return post_theme


async def make_cool_pic(input_array):
    corpus = await get_corpus(input_array)
    proc_word_cloud = await get_word_cloud(corpus)

    fig = plt.figure(figsize=(20, 8))
    plt.subplot(1, 2, 1)
    plt.imshow(proc_word_cloud)
    plt.axis('off')
    plt.subplot(1, 2, 1)
    fig.savefig(f"cloud{random.randint(111111, 999999)}.png", dpi=fig.dpi)

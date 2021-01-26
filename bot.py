import requests
import telebot
import urllib
from random import randint

from talk_to_back import BackendTalker

with open('token.txt', 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)
help = """
/start - Запустить бота
Для того, чтобы положить товар на склад, отправьте боту налкадную в формате .xlsx
Пример .xlsx файла можно получить командой /put
/get <имя ячеки, например, A1, либо uuid товара> - Забрать товар со склада
/searchcell <имя ячеки, например, A1> - Найти полку в системе
/searchitem <uuid> - Найти товар в системе
/scheme - Получить схему склада
/list - Получить список товаров и полок
/remote - Получить список товаров на удаленном складе
/help - Помощь с применением команд       
"""


# start - Запустить бота
# put - Положить товар на склад
# get - Забрать товар со склада
# searchcell - Найти полку в системе
# searchitem - Найти товар в системе
# scheme - Получить схему склада
# list - Получить список товаров и полок
# help - Помощь с применением команд

@bot.message_handler(commands=["start", "put", "get", "searchcell", "searchitem", "scheme", "list", "remote", "help"])
def get_commands_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Здравсвтуйте!")
        bot.send_message(message.from_user.id, text=help)

    elif message.text == "/put":
        bot.send_message(message.from_user.id, text="Отправьте мне файл в формате .xlsx")
        bot.send_message(message.from_user.id, text="Пример файла: ")
        _ex = open("/Users/ovsannikovaleksandr/Desktop/предпроф/bot/example.xlsx", "rb")
        bot.send_document(message.from_user.id, data=_ex)



    elif message.text.split()[0] == "/get":
        _text = message.text.split()
        if len(_text) != 2:
            bot.send_message(message.from_user.id, text="Неправильно введен аргумент")
        else:
            resp = talker.get(_text[-1])

            if resp == "Position is empty":
                bot.send_message(message.from_user.id, text="Запрашиваемая позиция пуста")
            elif resp == "NO SUCH UUID OR CELL NAME FOUND":
                bot.send_message(message.from_user.id,
                                 text="Позиция не найдена, проверьте правильность написания идентификатора")
            elif resp == "ERROR":
                bot.send_message(message.from_user.id, text="Произошла ошибка")
            elif resp == "OK":
                bot.send_message(message.from_user.id, text="Позиция выдана со склада")
                _img = open("/Users/ovsannikovaleksandr/Desktop/предпроф/back/static/img/scheme.png", "rb")
                bot.send_photo(message.from_user.id, photo=_img)


    elif message.text.split()[0] == "/searchcell":
        _text = message.text.split()
        if len(_text) != 2:
            bot.send_message(message.from_user.id, text="Неправильно введен аргумент")
        else:
            _cell = talker.get_cell(_text[-1])
            if _cell != "Неправильная ячейка":
                resp = f"Имя: {_cell.name}\n" \
                       f"Объединена: {'Да' if _cell.merged else 'Нет'}\n" \
                       f"Объединена с: {_cell.merged_with if _cell.merged else '-'}\n" \
                       f"Ширина: {_cell.size_width}\n" \
                       f"Высота: {_cell.size_height}\n" \
                       f"Глубина: {_cell.size_depth}\n\n" \
                       f"<b>Сведения о товаре:</b>\n" \
                       f"Занята товаром: {'Да' if _cell.busy else 'Нет'}\n" \
                       f"Название товара: {_cell.contained_item.name if _cell.contained_item else '-'}\n" \
                       f"UUID товара: {'<code>' + _cell.contained_item.uuid + '</code>' if _cell.contained_item else '-'}\n" \
                       f"Масса товара: {_cell.contained_item.mass if _cell.contained_item else '-'}"
                bot.send_message(message.from_user.id, text=resp, parse_mode="HTML")

            else:
                bot.send_message(message.from_user.id, text=_cell)

    elif message.text.split()[0] == "/searchitem":
        _text = message.text.split()
        if len(_text) != 2:
            bot.send_message(message.from_user.id, text="Неправильно введен аргумент")
        else:
            _cell = talker.get_data_to_search_by_item(_text[-1])
            if _cell != "Неправильный uuid":
                resp = f"Название товара: {_cell.contained_item.name if _cell.contained_item else '-'}\n" \
                       f"Масса товара: {_cell.contained_item.mass if _cell.contained_item else '-'}\n\n" \
                       f"<b>Сведения о полке:</b>\n" \
                       f"Имя полки: {_cell.name}\n" \
                       f"Объединена: {'Да' if _cell.merged else 'Нет'}\n" \
                       f"Объединена с: {_cell.merged_with if _cell.merged else '-'}\n" \
                       f"Ширина: {_cell.size_width}\n" \
                       f"Высота: {_cell.size_height}\n" \
                       f"Глубина: {_cell.size_depth}\n"
                bot.send_message(message.from_user.id, text=resp, parse_mode="HTML")

            else:
                bot.send_message(message.from_user.id, text=_cell)

    elif message.text == "/scheme":
        talker.get_scheme()
        _img = open("/Users/ovsannikovaleksandr/Desktop/предпроф/back/static/img/scheme.png", "rb")
        bot.send_photo(message.from_user.id, photo=_img)

    elif message.text == "/list":
        all_cells = talker.get_list_of_all()
        resp = ""
        for cell in all_cells:
            resp += f"Полка: {cell.name if not cell.merged else cell.merged_with}; Название товара:{cell.contained_item.name if cell.contained_item else 'Свободно'}; UUID товара: {'<code>' + cell.contained_item.uuid + '</code>' if cell.contained_item else '-'}; Масса товара: {cell.contained_item.mass if cell.contained_item else '-'} кг.\n\n"
        if len(resp) < 4096:
            bot.send_message(message.from_user.id, text=resp, parse_mode='HTML')
        else:
            for x in range(0, len(resp), 4096):
                bot.send_message(message.chat.id, resp[x:x + 4096], parse_mode="HTML")

    elif message.text == "/remote":
        resp = talker.get_remote()
        if resp == "":
            bot.send_message(message.from_user.id, text="Удаленный склад пуст")
        if len(resp) < 4096:
            bot.send_message(message.from_user.id, text=resp, parse_mode='HTML')
        else:
            for x in range(0, len(resp), 4096):
                bot.send_message(message.chat.id, resp[x:x + 4096], parse_mode="HTML")

    elif message.text == "/help":
        bot.send_message(message.from_user.id, text=help)


@bot.message_handler(content_types=["document"])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    print(message.document)
    if ".xlsx" in message.document.file_name:
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        print('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        bot.send_message(message.from_user.id, text="Добавляю товары на склад...")

        _data = talker.put(file.content).text.split(".")
        print(_data)
        _resp = _data[0]

        if _resp == "OK":
            bot.send_message(message.from_user.id, text="Товары из накладной добавлены на склад")
            _img = open("/Users/ovsannikovaleksandr/Desktop/предпроф/back/static/img/scheme.png", "rb")
            bot.send_photo(message.from_user.id, photo=_img)
        elif _resp == "CANNOT BE OPENED":
            bot.send_message(message.from_user.id, text="Не удалось открыть файл")

        else:
            bot.send_message(message.from_user.id, text="Произошла ошибка")


    else:
        bot.send_message(message.from_user.id, text="Формат файла не поддерживается")


talker = BackendTalker(host="192.168.0.109", port=3000)
bot.infinity_polling(interval=randint(0, 3))

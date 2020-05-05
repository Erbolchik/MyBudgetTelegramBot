import telebot
from telebot import types
import pandas as pd

bot=telebot.TeleBot('1293189035:AAGMMCKPxcwKrjFjvwzSZOv4KuF49dIy4FI') # токен для подключения


dictBudgetCategory=[]
dictBudgetPrice=[]

count=[0]
@bot.message_handler(commands=['start'])
def start_message(message):
    key = telebot.types.InlineKeyboardMarkup()
    but_1 = telebot.types.InlineKeyboardButton(text="Today", callback_data="Today")
    but_2 = telebot.types.InlineKeyboardButton(text="Statistics", callback_data="Statistics")
    but_3 = telebot.types.InlineKeyboardButton(text="Month", callback_data="Month")
    key.add(but_1, but_2)
    key.add(but_3)
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=key)






@bot.callback_query_handler(func=lambda c:True)
def start_message(c):
    if c.data == 'Today':
        if (len(dictBudgetPrice) == 0 or len(dictBudgetCategory) == 0):
            bot.send_message(c.message.chat.id, "НА СЕГОДНЯ ПОКА НЕТУ ТРАТ")
        else:
            textForToday=""
            bot.send_message(c.message.chat.id, "Сегодня затраты")
            for i in range(len(dictBudgetCategory)):
                textForToday+="Категория : "+dictBudgetCategory[i]+ ", Трата : "+dictBudgetPrice[i]+"\n"
            bot.send_message(c.message.chat.id, textForToday)
    if c.data == 'Month':
        if (len(dictBudgetPrice) == 0 or len(dictBudgetCategory) == 0):
            bot.send_message(c.message.chat.id, "НА ТЕКУЩИЙ МЕСЯЦ ПОКА НЕТУ ТРАТ")
        else:
            textForToday = ""
            bot.send_message(c.message.chat.id, "Месяц затраты")
            for i in range(len(dictBudgetCategory)):
                textForToday += "Категория : " + dictBudgetCategory[i] + ", Трата : " + dictBudgetPrice[i] + "\n"
            bot.send_message(c.message.chat.id, textForToday)
    if c.data == 'Statistics':
        dictionaryText = {'Category':[],
                          'Price': []}
        if(len(dictBudgetCategory)==0):
            bot.send_message(c.message.chat.id,"СНАЧАЛА ВВЕДИТЕ ДАННЫЕ О ЗАТРАТАХ")
        else:
            dictionaryText['Category']=dictBudgetCategory
            dictionaryText['Price']=dictBudgetPrice
            df = pd.DataFrame(dictionaryText, columns=['Category', 'Price'])
            df.to_excel(r'./data.xlsx', index=False, header=True)
            file=open('./data.xlsx', 'rb')
            bot.send_message(c.message.chat.id,"СТАТИСТИКА В EXCEL")
            bot.send_document(c.message.chat.id,file)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    arrayText=message.text.split()
    if(str(arrayText[0]).isdigit()==False):
        bot.send_message(message.chat.id,"СНАЧАЛА ВВЕДИТЕ СТОИМОСТЬ,ПОТОМ КАТЕГОРИЮ\n НАПРИМЕР ЕДА 500")
    else:
        key = telebot.types.InlineKeyboardMarkup()
        but_1 = telebot.types.InlineKeyboardButton(text="Today", callback_data="Today")
        but_2 = telebot.types.InlineKeyboardButton(text="Statistics", callback_data="Statistics")
        but_3 = telebot.types.InlineKeyboardButton(text="Month", callback_data="Month")
        key.add(but_1, but_2)
        key.add(but_3)
        dictBudgetPrice.append(arrayText[0])
        dictBudgetCategory.append(arrayText[1])
        temp=int(arrayText[0])
        count[0]+=temp
        bot.send_message(message.chat.id,'Сохранено')
        bot.send_message(message.chat.id,"Стоимость : "+str(arrayText[0])+"  "+str(arrayText[1])+"\n----\nэтот месяц: "+
                         str(count[0])+"\n"+"сегодня: "+str(count[0]),reply_markup=key)


bot.polling() # Отправка сообщения
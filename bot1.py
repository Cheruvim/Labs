#библиотеки
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
import pyowm


owm = pyowm.OWM('3d392c0d8cd4052041f077f91d0e3667')
TG_TOKEN = '922315303:AAGzSzrn5iR-V5PPa7Xbm4TtWxdKzm8bSKM' # bot token

#команда /start
def do_start(bot: Bot, update = Update):
	#тащим имя пользователя
	user = update.effective_user
	if user:
		name = user.first_name
	else:
		name = "anonym"
	#наши первые слова
	text = 'Input your town,pls'
	reply_text = f'Hi, {name}!\n\n{text}'

	bot.send_message(
		chat_id = update.effective_message.chat_id,
		text = reply_text
		)

	return
#сообщение пользователя(без команд) 
def temp(bot: Bot, update = Update):
	#город из сообщения юзера
	observation = owm.weather_at_place(update.effective_message.text)

	#запрос о погоде
	w = observation.get_weather()
	reg = owm.city_id_registry()
	#облегчаем(это можно делитнуть,но будет не удобно в выводу)
	city = reg.ids_for(update.effective_message.text)
	city = city[0][1]
	temp = w.get_temperature('celsius')['temp']
	status = w.get_detailed_status()
	humidity = w.get_humidity()
	wind = w.get_wind()['speed']
	#строка для вывода
	text = f'In {city}:\nTemperature: {temp}C.\nStatus: {status}.\nHumidity: {humidity}%.\nWind speed: {wind}m/s.'
	#вывод
	bot.send_message(
		chat_id = update.effective_message.chat_id,
		text = text
		)


def main():
	#инфра о боте
	bot = Bot(token = TG_TOKEN,
		base_url = "https://telegg.ru/orig/bot")
	updater = Updater(bot = bot)
	#что и когда делать
	start_handler = CommandHandler('start', do_start)
	temp_handler = MessageHandler(Filters.all, temp)
	#использем что и когда
	updater.dispatcher.add_handler(start_handler)
	updater.dispatcher.add_handler(temp_handler)
	#обновляем бота
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

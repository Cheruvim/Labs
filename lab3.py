#библиотеки
import requests
from bs4 import BeautifulSoup as BS
import os

#ссылка,откуда
link = 'https://student.mirea.ru'
htm = requests.get(link + '/media/photo')
html = BS(htm.content,'html.parser')

#выборка будет из html.select('')
for el in html.select('.js-slide'):

	#вытаскиваем ссылку
	a = requests.get(link + el.a.get('href'))

	#переходим по ссылке
	al = BS(a.content,'html.parser')

	#название альбомов и картинок
	os.makedirs(el.h3.text)
	name = os.path.abspath(el.h3.text)
	imge = 1

	#смотрим альбом
	for alb in al.select('.col-md-2'):
		#выделяем картинку
		img_link = link + alb.img.get('src')
		img = requests.get(img_link)

		#запись
		with open(name + "/" + str(imge) + ".jpg",'bw') as f:
			for chunk in img:
	 			f.write(chunk)

		imge += 1


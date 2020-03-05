#!/usr/bin/env python
# coding: utf-8

# # Этап 1. Получение данных

# Изучим данные, предоставленные сервисом для проекта.

# ## Импорт библиотек

# In[1]:


import pandas as pd


# Прочитаем файл *music_project.csv* и сохраним его в переменной *df*. 

# In[2]:


df = pd.read_csv('/datasets/music_project.csv')


# Получение первых 10 строк таблицы.

# In[3]:


df.head(10)


# Общая информация о данных таблицы *df*.
# 
# 
# 

# In[4]:


df.info()


# Рассмотрим полученную информацию подробнее.
# 
# Всего в таблице 7 столбцов, тип данных у каждого столбца - < напишите название типа данных >.
# 
# Подробно разберём, какие в *df* столбцы и какую информацию они содержат:
# 
# * userID — идентификатор пользователя;
# * Track — название трека;  
# * artist — имя исполнителя;
# * genre — название жанра;
# * City — город, в котором происходило прослушивание;
# * time — время, в которое пользователь слушал трек;
# * Day — день недели.
# 
# Количество значений в столбцах различается. Это говорит о том, что в данных есть <введите определение> значения.
# 
# 

# **Выводы**

# Каждая строка таблицы содержит информацию о композициях определённого жанра в определённом исполнении, которые пользователи слушали в одном из городов в определённое время и день недели. Две проблемы, которые нужно решать: пропуски и некачественные названия столбцов. Для проверки рабочих гипотез особенно ценны столбцы *time*, *day* и *City*. Данные из столбца *genre* позволят узнать самые популярные жанры.

# # Этап 2. Предобработка данных

# Исключим пропуски, переименуем столбцы, а также проверим данные на наличие дубликатов.

# Получаем перечень названий столбцов. Какая наблюдается проблема — кроме тех, что уже были названы ранее?

# In[5]:


df.columns


# В названиях столбцов есть пробелы, которые могут затруднять доступ к данным.

# Переименуем столбцы для удобства дальнейшей работы. Проверим результат.
# 
# 

# In[6]:


df.set_axis(['user_id', 'track_name', 'artist_name', 'genre_name', 'city', 'time', 'weekday'], axis='columns', inplace = True)


# In[7]:


print (df.info)


# Проверим данные на наличие пропусков вызовом набора методов для суммирования пропущенных значений.

# In[8]:


df.isnull


# Пустые значения свидетельствуют, что для некоторых треков доступна не вся информация. Причины могут быть разные: скажем,  не назван конкретный исполнитель народной песни. Хуже, если проблемы с записью данных. Каждый отдельный случай необходимо разобрать и выявить причину.

# Заменяем пропущенные значения в столбцах с названием трека и исполнителя на строку 'unknown'. После этой операции нужно убедиться, что таблица больше не содержит пропусков.

# In[9]:


df.isnull().sum()


# In[10]:


df['track_name'] = df['track_name'].fillna('unknown') 


# In[11]:


df['artist_name'] = df['artist_name'].fillna('unknown')


# In[12]:


df.isnull().sum()


# Удаляем в столбце с жанрами пустые значения; убеждаемся, что их больше не осталось.

# In[13]:


df = df.dropna()


# In[14]:


df.isnull().sum()


# Необходимо установить наличие дубликатов.  Если найдутся, удаляем, и проверяем, все ли удалились.

# In[15]:


df.duplicated().sum


# In[16]:


df = df.drop_duplicates().reset_index(drop=True)


# In[17]:


df.duplicated().sum()


# Дубликаты могли появиться вследствие сбоя в записи данных. Стоит обратить внимание и разобраться с причинами появления такого «информационного мусора».

# Сохраняем список уникальных значений столбца с жанрами в переменной *genres_list*. 
# 
# Объявим функцию *find_genre()* для поиска неявных дубликатов в столбце с жанрами. Например, когда название одного и того же жанра написано разными словами.
# 
# 
# 
# 

# In[18]:


genres_list = df['genre_name'].unique()


# In[19]:


def find_genre (genre_name):
    counter = 0
    for i in genres_list:
        if i == genre_name:
            counter+=1
    return counter
    


# Вызов функции *find_genre()* для поиска различных вариантов названия жанра хип-хоп в таблице.
# 
# Правильное название — *hiphop*. Поищем другие варианты:
# 
# * hip
# * hop
# * hip-hop
# 

# In[20]:


find_genre ('hip') 


# In[21]:


find_genre ('hop') 


# In[22]:


find_genre ('hip-hop') 


# Объявим функцию *find_hip_hop()*, которая заменяет  неправильное название этого жанра в столбце *'genre_name'* на *'hiphop'* и проверяет успешность выполнения замены.
# 
# Так исправляем все варианты написания, которые выявила проверка.

# In[23]:


def find_hip_hop(df, wrong):
    df['genre_name'] = df['genre_name'].replace (wrong, 'hiphop')
    result = df[df['genre_name'] == wrong]['genre_name'].count()
    return result 


# In[24]:


find_hip_hop (df, 'hip')


# Получаем общую информацию о данных. Убеждаемся, что чистка выполнена успешно.

# In[25]:


df.info()


# **Вывод**

# На этапе предобработки в данных обнаружились не только пропуски и проблемы с названиями столбцов, но и всяческие виды дубликатов. Их удаление позволит провести анализ точнее. Поскольку сведения о жанрах важно сохранить для анализа, не просто удаляем все пропущенные значения, но заполним пропущенные имена исполнителей и названия треков. Имена столбцов теперь корректны и удобны для дальнейшей работы.

# # Действительно ли музыку в разных городах слушают по-разному?

# Была выдвинута гипотеза, что в Москве и Санкт-Петербурге пользователи слушают музыку по-разному. Проверяем это предположение по данным о трёх днях недели — понедельнике, среде и пятнице.
# 
# Для каждого города устанавливаем количество прослушанных  в эти дни композиций с известным жанром, и сравниваем результаты.

# Группируем данные по городу и вызовом метода *count()* подсчитываем композиции, для которых известен жанр.

# In[26]:


df.groupby('city')
df['genre_name'].count()


# В Москве прослушиваний больше, чем в Питере, но это не значит, что Москва более активна. У Яндекс.Музыки в целом больше пользователей в Москве, поэтому величины сопоставимы.

# Сгруппируем данные по дню недели и подсчитаем прослушанные в понедельник, среду и пятницу композиции, для которых известен жанр.

# In[27]:


df.groupby('weekday')
df['genre_name'].count()


# Понедельник и пятница — время для музыки; по средам пользователи немного больше вовлечены в работу.

# Создаём функцию *number_tracks()*, которая принимает как параметры таблицу, день недели и название города, а возвращает количество прослушанных композиций, для которых известен жанр. Проверяем количество прослушанных композиций для каждого города и понедельника, затем среды и пятницы.

# In[28]:


def number_tracks(df, day, city):
    track_list = df[(df['weekday'] == day) & (df['city'] == city)]
    track_list_count = track_list['genre_name'].count()
    return track_list_count


# In[29]:


number_tracks(df, 'Monday', 'Moscow')


# In[30]:


number_tracks(df, 'Monday', 'Saint-Petersburg')


# In[31]:


number_tracks(df, 'Wednesday', 'Moscow')


# In[32]:


number_tracks(df, 'Wednesday', 'Saint-Petersburg')


# In[33]:


number_tracks(df, 'Friday', 'Moscow')


# In[34]:


number_tracks(df, 'Friday', 'Saint-Petersburg')


# Сведём полученную информацию в одну таблицу, где ['city', 'monday', 'wednesday', 'friday'] названия столбцов.
# 

# In[35]:


columns = ['city', 'monday', 'wednesday', 'friday']
data = [['Moscow', 15347, 10865, 15680], ['Saint-Petersburg', 5519, 6913, 5802]]
table = pd.DataFrame(data=data, columns = columns) 


# **Вывод**

# Результаты показывают, что относительно среды музыку в Петербурге и Москве слушают «зеркально»: в Москве пики приходятся на понедельник и пятницу, а в среду время прослушивания снижается. Тогда как в Санкт-Петербурге среда — день самого большого интереса к музыке, а в понедельник и пятницу он меньше, причём почти одинаково меньше.

# # Утро понедельника и вечер пятницы — разная музыка или одна и та же?

# Ищем ответ на вопрос, какие жанры преобладают в разных городах в понедельник утром и в пятницу вечером. Есть предположение, что в понедельник утром пользователи слушают больше бодрящей музыки (например, жанра поп), а вечером пятницы — больше танцевальных (например, электронику).

# Получим таблицы данных по Москве *moscow_general* и по Санкт-Петербургу *spb_general*.

# In[36]:


moscow_general = df[df['city']=='Moscow']


# In[37]:


spb_general = df[df['city']=='Saint-Petersburg']


# Создаём функцию *genre_weekday()*, которая возвращает список жанров по запрошенному дню недели и времени суток с такого-то часа по такой-то.

# In[38]:


def genre_weekday(df, day, time1, time2):
    genre_list = df[(df['weekday'] == day) & (df['time'] > time1) & (df['time'] < time2)]
    genre_lst_sorted = genre_list.groupby('genre_name')['genre_name'].count()
    genre_list_sorted = genre_lst_sorted.sort_values(ascending = False).head(10)
    return genre_list_sorted


# Cравниваем полученные результаты по таблице для Москвы и Санкт-Петербурга в понедельник утром (с 7 до 11) и в пятницу вечером (с 17 до 23).

# In[39]:


genre_weekday (moscow_general, 'Monday','07:00:00', '11:00:00')


# In[40]:


genre_weekday(spb_general, 'Monday', '07:00:00', '11:00:00')


# In[41]:


genre_weekday (moscow_general, 'Friday','17:00:00', '23:00:00')


# In[42]:


genre_weekday(spb_general, 'Friday', '17:00:00', '23:00:00')


# Популярные жанры в понедельник утром в Питере и Москве оказались похожи: везде, как и предполагалось, популярен поп. Несмотря на это, концовка топ-10 для двух городов различается: в Питере в топ-10 входит джаз и русский рэп, а в Москве жанр *world*.
# 
# В конце недели ситуация не меняется. Поп-музыка всё так же на первом месте. Опять разница заметна только в концовке топ-10, где в Питере пятничным вечером тоже присутствует жанр *world*.

# **Вывод**

# Жанр поп безусловный лидер, а топ-5 в целом не различается в обеих столицах. При этом видно, что концовка списка более «живая»: для каждого города выделяются более характерные жанры, которые действительно меняют свои позиции в зависимости от дня недели и времени.

# # Москва и Питер — две разные столицы, два разных направления в музыке. Правда?

# Гипотеза: Питер богат своей рэп-культурой, поэтому это направление там слушают чаще, а Москва — город контрастов, но основная масса пользователей слушает попсу.
# 
# 

# Сгруппируем таблицу *moscow_general* по жанру, сосчитаем численность композиций каждого жанра методом *count()*, отсортируем в порядке убывания и сохраним результат в таблице *moscow_genres*.
# 
# Просмотрим первые 10 строк этой новой таблицы.

# In[43]:


mg=moscow_general.groupby('genre_name')['genre_name'].count()
moscow_genres = mg.sort_values(ascending = False)


# In[44]:


moscow_genres.head(10)


# Сгруппируем таблицу *spb_general* по жанру, сосчитаем численность композиций каждого жанра методом *count()*, отсортируем в порядке убывания и сохраним результат в таблице *spb_genres*.
# 
# Просматриваем первые 10 строк этой таблицы. Теперь можно сравнивать два города.

# In[45]:


spbb=spb_general.groupby('genre_name')['genre_name'].count()
spb_genres = spbb.sort_values(ascending = False)


# In[46]:


spb_genres.head(10)


# **Вывод**

# В Москве, кроме абсолютно популярного жанра поп, есть направление русской популярной музыки. Значит, что интерес к этому жанру шире. А рэп, вопреки предположению, занимает в обоих городах близкие позиции.

# # Этап 4. Результаты исследования
# 

# Рабочие гипотезы:
# 
# * музыку в двух городах — Москве и Санкт-Петербурге — слушают в разном режиме;
# 
# * списки десяти самых популярных жанров утром в понедельник и вечером в пятницу имеют характерные отличия;
# 
# * население двух городов предпочитает разные музыкальные жанры.
# 
# **Общие результаты**
# 
# Москва и Петербург сходятся во вкусах: везде преобладает популярная музыка. При этом зависимости предпочтений от дня недели в каждом отдельном городе нет — люди постоянно слушают то, что им нравится. Но между городами в разрезе дней неделей наблюдается зеркальность относительно среды: Москва больше слушает в понедельник и пятницу, а Петербург наоборот - больше в среду, но меньше в понедельник и пятницу.
# 
# В результате первая гипотеза < укажите подтверждена/не подтверждена>, вторая гипотеза < укажите подтверждена/не подтверждена > и третья < укажите подтверждена/не подтверждена >.

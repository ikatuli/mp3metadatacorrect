'''
Публичная лицензия этого продукта 
Copyright © 2022 ikatuli
При использовании данного продукта вы соглашаетесь со следующими пунктами лицензии:
1. Вы имеете право делать с данным продуктом всё что угодно, за исключением того, что может являться нарушением законов страны, в которой находитесь вы, или страны, в которой этот продукт будет использоваться.
2. Автор не несёт ответственности за какой-либо прямой, непрямой, особый или иной косвенный ущерб нанесённый в результате использования, не использования и существования продукта.
'''

import eyed3 
from sys import argv
from os.path import basename, getctime, getatime, exists
from os import utime

def str_refinement(string): #Функция удаляет пробелы в конце и начале строки, а так же редактирует строку, что бы каждое слово начиналось с большой буквы
    string=string.strip()
    string=string.title()
    return string

def file_tage (string): #Обработка строки на два тега
    if string.find('.mp3')!=-1:
        string=string[:len(string)-4] #Удаляем расширение
    index=string.find(' - ')
    if index!=-1: #Если мы нашли тире с пробелами
        tag=[string[:index],string[index+3:]] #Делим строки на две части по первому тире. 
    else:
        tag=['',string]
    #tag=string.split('-') # Делим строку на части по тире.
    tag=list(map(str_refinement,tag)) # обрабатываем строки
    return tag

# основной блок
argv.pop(0) #Нулевой параметр нам не нужен
eyed3.log.setLevel("ERROR") #Выводить только ошибки

for i in argv: #Перебор всех отданных файлов

    mp3file=None #На всякий пожарный обнуляем.
    titlefile=None
    time=None
    
    time=(getatime(i),getctime(i)) #Сохраняем дату последнего доступа и последнего изменения времени.

    if exists(i): # На всякий пожарный проверим существование файла
        mp3file=eyed3.load(i) #Грузим теги из файла

    if not(mp3file): #Некоторые файлы не читаются и тогда приходится из пропускать. Попробуйте вручную добавить этим файлам теги через vlc.
        print("Файл '", i ,"' пропущен",sep="")
        continue

    if not(mp3file.tag): #Создаём тег, если он отсутствовал.
        mp3file.initTag()

    titlefile=file_tage(basename(i)) # Получаем теги из названия файла
        
    if not(mp3file.tag.artist) and mp3file.tag.title: #Если есть только название, но нет исполнителя
        #Иногда в треке и автор и песня находятся в теге "название"
        if (mp3file.tag.title.find(' - ')!=-1): # Если в названии песни есть разделитель
            titlefile=file_tage(mp3file.tag.title)

    if titlefile: #Если в titlefile попало значение.
        # Перезаписываем тег только если он пустой
        if not(mp3file.tag.artist):
            mp3file.tag.artist=titlefile[0]
        if not(mp3file.tag.title):
            mp3file.tag.title=titlefile[1]
        mp3file.tag.save()
        utime(i,time) #восстанавливаем прежнее время


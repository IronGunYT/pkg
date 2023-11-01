# [ПКГ] Лабораторная работа 2 - Чтение информации из графических файлов

Для разработки использовался язык Python, для отображения графики - tkinter, для анализа изображений - Pillow

## Описание работы

В созданном интерфейсе пользователю предоставляется возможность выбора папки с файлами(плоским списком)

После чего путь к выбранной папке отобразиться в Label, для анализа файлов следует нажать кнопку Process

После чего в таблице отобразится список файлов с полями:
* Filename - имя файла
* Size - ширина и высота(в пикселях)
* Resolution - разрешение(dpi) - ширина и высота
* Depth - глубина цвета
* Compression - сжатие
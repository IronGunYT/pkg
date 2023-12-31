# Image Processing Application

Приложение представляет собой простой графический интерфейс, который позволяет пользователям загружать изображения и применять различные фильтры обработки изображений.
Ниже приведено описание функциональности приложения. Приложение предназначено для загрузки изображения, применения различных фильтров обработки изображений и отображения отфильтрованных изображений.

## Зависимости

Проект использует Python3 с следующими зависимостями:

- `tkinter`
- `cv2`
- `PIL`
- `numpy`

## Описание функций обработки изображений

### Функции

1. `global_thresholding`: Функция выполняет глобальную пороговую обработку для входного изображения. Она принимает изображение и порог в качестве
    параметров. Она преобразует изображение в черно-белое, присваивая значениям пикселей, большим пороговому значению, значение
    255 (белый) и значениям пикселей, меньшим пороговому значению, значение 0 (черный).
2. `global_thresholding_otsu`: Функция выполняет глобальную пороговую обработку для входного изображения. Она принимает изображение в качестве параметра.
    Она преобразует изображение в черно-белое, присваивая значениям пикселей, большим пороговому значению, значение 255 (белый)
    и значениям пикселей, меньшим пороговому значению, значение 0 (черный). Она использует метод Оцу для определения порогового
    значения.
3. `adaptive_thresholding`: Функция выполняет адаптивную пороговую обработку для входного изображения. Она принимает изображение в качестве параметра.
    Она преобразует изображение в черно-белое, выполняя адаптивную пороговую обработку с размером блока 11
4. `high_pass_filter`: Функция принимает изображение и возвращает результат применения фильтра повышения резкости с заданной матрицей.

### Основные возможности приложения

1. Пользователи могут выбрать изображение, нажав кнопку "Browse". После выбора изображение отображается на главном экране приложения.

2. Пользователи могут выбрать фильтр из списка доступных фильтров в левом меню. После выбора фильтра и нажатия кнопки "Apply Filter" изображение обрабатывается выбранным фильтром и отображается на главном холсте.

3. В приложении доступны следующие фильтры: глобальная пороговая обработка, адаптивная пороговая обработка, фильтр повышения резкости с разными параметрами.

## Использование приложения

Для запуска приложения используется библиотека tkinter. В основном окне приложения есть холст для отображения обработанных изображений и кнопки для загрузки изображений и применения фильтров.

Чтобы начать, откройте приложение и выберите изображение с помощью кнопки "Browse". Затем выберите один из фильтров и нажмите "Apply Filter", чтобы увидеть обработанный результат.

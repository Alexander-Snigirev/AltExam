# AltExam
#### Описание

Реализация алгоритма ```Chu-Liu-Edmonds``` поиска минимального остовного дерева в ориентированном графе с визуализацией.
#### Инструкция по запуску
1. Установите необходимые модули
   
   ```pip install -r requirements.txt```
2. В рабочем каталоге создайте текстовый файл. Сохраните в нем граф в формате:

   ```
   <Число вершин> <Число ребер>
   <Начало ребра 1> <Конец ребра 1> <Вес ребра 1>
   ...
   <Начало ребра m> <Конец ребра m> <Вес ребра m>
   <Корень дерева>
   ```

   Имя файла сохраните в константу ```FNAME``` файла ```config.py```
3. В константу ```VIZ_DIR``` файла ```config.py``` сохраните имя директории, в которую будет загружена визуализация
4. Запустите программу командой
   
   ```python3 main.py```
   
   

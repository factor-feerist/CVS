# CVS
Оффлайн ситема контроля версий. Авторы: Сыч Эрнест, Романов Виталий
## Запуск
Работа с системой осуществляется через консоль, для запуска просто откройте файл shell.py
## Набор комманд
### ?
    > ?
    Выдает список доступных команд
### help
    > help 'команда'
    выдаст подсказку по использованию команды
### cd
    > cd 'путь до директории'
    меняет текущую директорию на указанную. Можно использовать как полный путь,
    так и просто название директории, если она лежит внутри текущей
### mkdir
    > mkdir 'директория'
    создает директорию в текущей директории
### touch
    > touch 'файл'
    создает файл в текущей директории
### ls
    > ls
    показывает список всех директорий и файлов, лежащих в текущей директории
### init
    > init
    Инициализирует репозиторий в текущей директории
### add
    > add 'файл1' 'файл2' ... 'директория 1' 'директория 2' ...
    добавляет перечисленные файлы и файлы из перечисленных директорий в stage
    > add .
    добавляет все файлы в текущей директории в stage
### commit
    > commit 'сообщение'
    создает коммит изменений в stage с указанным сообщением
### branch
    > branch 'имя'
    создает ветку с указанным именем (привязывается к текущему коммиту)
    > branch 'имя' r
    удаляет ветку с указанным именем
### slog
    > slog
    показывает список изменений stage
### clog
    > clog
    показывает список коммитов с изменениями
### tag
    > tag 'имя' 'сообщение'
    создает тег с указанным именем и сообщением (привязывается к текущему коммиту)
    > tag 'имя' r
    удаляет тег с указанным именем
### tlog
    > tlog
    показывает список тегов с сообщениями
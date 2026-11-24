# BTD6 Money Cheat — запуск одним кликом

## Самый простой способ (рекомендую)
1. Установи Python 3 один раз: https://www.python.org/downloads/
   (при установке поставь галочку "Add Python to PATH")
2. Скачай файл launch.pyw из этого репозитория (кнопка Code -> Download ZIP, внутри папка launcher).
3. Двойной клик по launch.pyw -> откроется окошко -> жми "Установить и запустить".
   Скрипт сам:
   - найдёт папку игры Steam,
   - скачает официальный мод-загрузчик NML с GitHub,
   - установит его и мод MoneyCheat.zip,
   - запустит игру.
4. В игре нажми F8 = +$10 000.

Хочешь .exe без Python — после установки Python выполни в папке launcher:
   pip install pyinstaller
   pyinstaller --onefile --noconsole --name MoneyCheatLauncher launch.pyw
Готовый exe появится в launcher\dist\. Я собрать exe из этой песочницы не могу — только под Windows.

## Ручной способ (без скрипта)
1. NML: https://github.com/Natechillton/Mod-Loader/releases -> скачать BTD6.zip -> распаковать в папку игры (рядом с BloonsTD6.exe).
2. MoneyCheat.zip -> положить в папку игры в Mods\ (не распаковывая).
3. Запустить игру, включить мод в меню N-Mods, F8 = деньги.

## Важно
- Steam может "чинить" файлы игры — лучше скопировать папку игры и запускать exe напрямую.
- Только оффлайн, мультиплеер не трогай.

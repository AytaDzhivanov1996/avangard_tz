# Инструкция  для запуска
1. Клонируем репозиторий: git clone git@github.com:AytaDzhivanov1996 avangard_tz.git
2. Устанавливаем зависимости: pip install -r requirements.txt
3. Меняем переменные окружения
4. Создаем и применяем миграции: flask db init, flask db migrate, flask db upgrade
5. Запуск: flask run --reload
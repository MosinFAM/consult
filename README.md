# Тут будет небольшое руководство, описание команд и пр.

Возможно что-то будет описано неполно или неверно, в таком случае будем исправлять

## Клонирование репозитория

```bash
git clone https://github.com/MosinFAM/consult.git
```

## Основная работа

```bash
# Создаем виртуальное окружение (например, с использованием venv)
python -m venv venv

# Активируем виртуальное окружение

# Для Windows:
venv\Scripts\activate

# Для macOS/Linux:
source venv/bin/activate

# Устанавливаем зависимости из requirements.txt
pip install -r requirements.txt

# Переключаемся на нужную ветку
# Перед началом работы обязательно создайте свою ветку от основной (например, feature-branch):
git checkout -b feature-branch

# Вносим изменения в код

# Добавляем новые зависимости в requirements.txt (если есть)
pip freeze > requirements.txt
```


## Работа с Git

```bash
# Подтянуть последние изменения из основной ветки (main) перед коммитом
# Чтобы избежать конфликтов и всегда работать с актуальной версией кода:
git checkout main
git pull origin main
git checkout feature-branch
git rebase main

# Примечание: Если при ребейзе возникнут конфликты, их нужно вручную разрешить, после чего продолжить ребейз командой:
git rebase --continue

# Добавляем изменения в индекс
git add .

# Коммитим изменения с понятным описанием
git commit -m "Краткое описание изменений"

# Отправляем изменения в свою ветку на удаленный репозиторий
git push origin feature-branch

# После завершения работы и тестирования откройте Pull Request для слияния изменений с основной веткой. Ожидайте ревью от коллег перед слиянием.
```


## Возможные ошибки

Error: That port is already in use. (Linux точно работает, если нет - гуглите)
```bash
sudo lsof -t -i tcp:8000 | xargs kill -9
```

## Основные команды в Django

Основные команды представлены здесь - https://www.reg.ru/blog/shpargalka-po-python-dlya-django/
Думаю, двух приложений: users и main (во втором будет основная логика работы с курсами) нам достаточно.



python manage.py loaddata data.json
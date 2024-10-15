from bs4 import BeautifulSoup


def enhance_html(html_content):
    """
    Функция для обработки HTML-контента.
    Увеличивает текст, добавляет отступы по бокам и добавляет открытие ссылок в новой вкладке, если это еще не сделано.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Стиль с увеличением шрифта и отступами
    new_style = """
    <style>
        p {
            font-size: 20px;
            margin-left: 20px;
            margin-right: 20px;
        }
        ul {
            font-size: 20px;
            margin-left: 20px;
            margin-right: 20px;
        }
        li {
            font-size: 20px;
            margin-left: 20px;
            margin-right: 20px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    """

    # Проверка на наличие аналогичного стиля
    style_already_exists = False
    for style_tag in soup.find_all('style'):
        if new_style.strip() in style_tag.decode_contents():
            style_already_exists = True
            break

    # Если стиль не найден, добавляем его в <head>
    if not style_already_exists:
        if soup.head:
            soup.head.append(BeautifulSoup(new_style, 'html.parser'))
        else:
            head_tag = soup.new_tag('head')
            head_tag.append(BeautifulSoup(new_style, 'html.parser'))
            soup.insert(0, head_tag)

    # Добавляем атрибут target="_blank" ко всем ссылкам <a>, если он еще не установлен
    for a_tag in soup.find_all('a'):
        if not a_tag.get('target') == '_blank':
            a_tag['target'] = '_blank'

    return str(soup)

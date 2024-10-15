from bs4 import BeautifulSoup


def enhance_html(html_content):
    """
    Функция для обработки HTML-контента.
    Увеличивает текст и добавляет отступы по бокам.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Стиль с увеличением шрифта и отступами
    style = """
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

    # Добавляем стиль в <head> или создаем <head>, если его нет
    if soup.head:
        soup.head.append(BeautifulSoup(style, 'html.parser'))
    else:
        head_tag = soup.new_tag('head')
        head_tag.append(BeautifulSoup(style, 'html.parser'))
        soup.insert(0, head_tag)

    return str(soup)

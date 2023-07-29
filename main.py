from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# настройки запуска
hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """ Класс управления web-сервером   """

    def __get_index(self):
        """ Метод возвращает данные индексной страницы   """
        return """
        <html><head><title>Blog</title></head><body>
        <h1>Lorem blog</h1>
        <ul>
        <li><a href='/?page=news1'>New one</a></li>
        <li><a href='/?page=news2'>New two</a></li>
        <li><a href='/?page=news3'>New three</a></li>
        </ul>
        </body>
        </html>
        """

    def __get_article_content(self, page_address):
        """ Метод возвращает текст статьи   """
        if page_address == 'news1':
            return 'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. '
        elif page_address == 'news2':
            return 'Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus, qui blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, qui officia deserunt mollitia animi, id est laborum et dolorum fuga.'
        elif page_address == 'news3':
            return 'Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit, quo minus id, quod maxime placeat, facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet, ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.'

        return 'Article not found!'

    def __get_blog_article(self, page_address):
        """ Метод возвращает страницу блога  """
        return f"""
        <html><head><title>Blog</title></head><body>
        <a href="/">Back</a><br>
        <p>{self.__get_article_content(page_address)}</p>
        </body>
        </html>
        """

    def do_GET(self):
        """ Метод обработки GET-запросов """
        query_components = parse_qs(urlparse(self.path).query)  # парсинг url
        page_address = query_components.get('page')
        page_content = self.__get_index()  # данные страницы
        if page_address:
            page_content = self.__get_blog_article(page_address[0])
        self.send_response(200)  # отправка кода ответа 200 (OK)
        self.send_header("Content-type", "text/html")  # отправка типа данных, который будет передаваться: text/html
        self.end_headers()  # завершение формирования заголовков ответа
        self.wfile.write(bytes(page_content, "utf-8"))  # тело ответа


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")

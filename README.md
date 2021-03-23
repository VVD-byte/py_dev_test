# py_dev_test
url api - ```***/api/v1```
Регистрация и авторизация - BasicAuth <br />
```/register/``` - регистрация. Метод POST, входные данные QueryParams (username, email, password) <br />
```/purse/``` - получить счета - метод GET, входные данные QueryParams нет <br />
```/purse/``` - добавить счет - метд POST, входные данные QueryParams (name) <br />
```/purse/``` - обновить счет (можно обновить только имя) - метод PUT, входные данные QueryParams (id-id счета, new_name) <br />
```/purse/``` - удалить счет (не возможно при балансе != 0) - метод DELETE, входные данные QueryParams (id-id счета) <br />
```/trans/``` - получить транзакции - метод GET, входные данные QueryParams (purse - не обязательный id счета для фильтрации транзакций) <br />
```/trans/``` - добавить транзакцию - метд POST, входные данные QueryParams (purse - id счета, money, comment - не обязательный параметр) <br />
```/trans/``` - метод PUT отсутствуе, т.к нет данных, которые можно обновлять
```/trans/``` - удалить счет (не возможно при балансе != 0) - метод DELETE, входные данные QueryParams (trans_id) <br />
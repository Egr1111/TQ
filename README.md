<h1 align="center">README.md API <Название></h1>

<h3>http://127.0.0.1:8000/v1/api/ - основной адрес этого API</h3>
<h3>Он имеет следующие команды:</h3>
<ul>
<li>/users/ - выводит данные всех пользователей о том, кто ввел их иинвайт ключ</li>
<li>GET /login/ - выводит данные о том, кто ввел инвайт ключ текущего авторизованного пользователя</li>
<li>POST /login/ data={"username": +70000000000, "password": "QWER"} - высылает код на номер в "username", если между вызовами этой функции прошло меньше 1 минуты и авторизует пользователя "username" по паролю из "password" в противном случае.</li>
<li>POST /createUser/ data={"username": +70000000000} - создает нового неавторизованного пользователя по номеру из "username"</li>
<li>GET /logout/ - закрывает сессию текущего авторизованного пользователя</li>


</ul>
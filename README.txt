admins:
	first_name:K
	last_name:S
	login:admin@mirea.ru
	password:admin

staff:
	first_name:Андрей cергеевич
	last_name:Зуев
	login:zuev@mirea.ru
	password:keklolkek

	first_name:Максудбек
	last_name:Игамбердыев
	login:maksudbek@mirea.ru
	password:keklolkek

users:

	first_name:Иван
	last_name:Малов
	login:malov@mirea.ru
	password:keklolkek
	
	first_name:Роман
	last_name:Суринов
	login:surinov@mirea.ru
	password:keklolkek

available urls:
http://localhost:8000/api/user_list/			выводит список всех пользователей		permission:admin,staff
http://localhost:8000/api/own_record_list/		выводит список своих записей			permission:authenticated
http://localhost:8000/api/add_record/			добавление записи				permission:authenticated
http://localhost:8000/api/update_record/<int:pk>/	проверка и оценивание записи			permission:admin,staff
http://localhost:8000/api/hire/				наем staff,admin				permission:admin
http://localhost:8000/api/fire/				увольнение staff,admin				permission:admin
# Referral System
## Тестовое задание для "Hammer Systems"

Проект развёрнут на _pythonanywhere.com_:

Админка (логин: admin, пароль: admin):

https://tanjaov.pythonanywhere.com/admin/

Cпецификации API (подробные, включают описание ошибок):

https://tanjaov.pythonanywhere.com/api/v1/swagger/

https://tanjaov.pythonanywhere.com/api/v1/redoc/

Коллекция запросов в Postman:

https://www.postman.com/tanja-ovc/workspace/hammer-systems/collection/17781130-606670c6-b29f-42ab-850c-a25da4da7cfa

### Стек

Python 3.11, Django 4.2, DRF 3.15, SQLite*

*SQLite выбрана вместо PostgreSQL, чтобы не доплачивать за PostgreSQL на _pythonanywhere.com_

### Описание API

```POST /api/v1/auth/phone/``` - пользователь вводит номер телефона и отправляет его. Номер валидируется на предмет соответствия формату (6 символов, только цифры и латинские буквы). Если номер новый, он записывается в БД + создаётся invite-код и ассоциируется с этим новым номером (пользователем). Дальше, вне зависимости от того, новый номер или уже существующий в БД, для него генерируется код подтверждения. Поскольку код подтверждения не отправляется по-настоящему на телефон, для удобства тестирования я поместила его в ответ:

<img width="490" alt="Screenshot 2024-04-23 at 03 22 22" src="https://github.com/tanja-ovc/referral-system/assets/85249138/7b3eb82b-76dd-4f27-95ba-4f56543623f9">

```POST /api/v1/auth/phone/confirm/``` - пользователь вводит код подтверждения и отправляет его. Код валидируется на предмет соответствия формату (4 цифры), проверяется на существование. Если всё ок, происходит псевдоаутентификация: в модели пользователя ставится флаг "аутентифицирован".

Поскольку настоящей аутентификации не происходит, дальнейшие запросы делаются не от первого лица пользователя, а "для" пользователя по его id.

```POST /api/v1/users/{id}/activate_invite_code/``` - для пользователя, получившего от другого пользователя инвайт-код, вводится полученный инвайт-код и отправляется на активацию.
Предусмотрены проверки того, чтобы:
- код был валидным (6 символов, только цифры и латинские буквы),
- код существовал (был присвоен какому-то пользователю, но не тому, который производит активацию),
- для пользователя, уже активировавшего один инвайт-код, не мог быть активирован другой инвайт-код.

```POST /api/v1/users/{id}/profile/``` - получение профиля пользователя. Содержит в том числе информацию о том, кто активировал инвайт-код, принадлежащий запрашиваемому пользователю:

<img width="257" alt="Screenshot 2024-04-23 at 03 41 56" src="https://github.com/tanja-ovc/referral-system/assets/85249138/ace012b6-1430-484a-93e9-b82f9ecdc396">

### P. S.

В базе данных оставляю несколько записей - возможно, так будет удобнее.

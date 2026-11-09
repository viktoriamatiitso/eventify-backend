# Eventify - Платформа для купівлі квитків на події

## 📖 Опис та бізнес-логіка сайту

**Eventify** - це сайт для перегляду та купівлі квитків на різноманітні культурні та розважальні заходи (концерти, стендапи, театральні вистави, тощо). Сайт допомагає користувачам швидко знаходити цікаві події, фільтрувати їх за категоріями, майданчиками чи артистами, переглядати детальний опис заходу та купувати квитки.

### Що є на сайті з точки зору бізнес-логіки:
- **Каталог подій:**  Головна сторінка зі списком усіх заходів, пошуком за назвою, фільтрами (за категорією, майданчиком, тощо) та сортуванням (за ціною, датою проведення чи популярністю).
- **Сторінка події:**  Детальна інформація про конкретний захід, дата і час, вартість квитка, інформація про виконавця та локацію, а також кнопка купівлі.
- **Сторінка артистів:**  Список усіх виконавців/артистів. При переході на сторінку конкретного артиста відображаються всі його майбутні події.
- **Сторінка майданчиків (локацій):**  Перелік концертних залів, клубів чи театрів із можливістю переглянути події, які там відбуватимуться.
- **Авторизація та профіль:**  Можливість зареєструватися, зайти в акаунт, редагувати особисті дані та переглядати історію купівлі квитків.
- **Кошик і замовлення:**  Можливість додавати квитки на події в кошик та створювати замовлення однією кнопкою.
- **Інформаційна сторінка (Про нас):**  Контактні дані платформи, інформація про правила відвідування заходів та умови повернення квитків.

---

## 🔐 Аутентифікація, Авторизація та JWT

Для доступу до захищених ендпоінтів використовується **JWT (JSON Web Token)** механізм автентифікації. 

### Як передавати токен у заголовках (Headers):
Усі захищені запити вимагають наявності заголовка `Authorization` у такому форматі:
```http
Authorization: Bearer <ваш_access_token>
```

--- 

## ⚙️ Архітектура REST API

Усі запити та відповіді передаються у форматі **JSON**.

### 📌 Endpoint: Події (Events)
- **GET `/api/events`**
  - *Опис:* Отримати список усіх подій з можливістю пошуку, фільтрації та сортування.
  - *Query Parameters:* `search`, `category_id`, `venue_id`, `sort_by`.
  - *Response Status:* 200 OK
  - *Response Body:* 
    ```json
    [
      {
        "id": 3,
        "title": "Чуттєвий виступ Нікова",
        "description": "Ліричні треки та атмосферний вокал у затишному залі.",
        "price": "550.00",
        "date": "2026-11-04T19:00:00Z",
        "category": {
          "id": 1,
          "name": "Концерти"
        },
        "artist": {
          "id": 1,
          "name": "Ніков",
          "description": "Молодий український виконавець, автор чуттєвих треків.",
          "events": [
            {
              "id": 3,
              "title": "Чуттєвий виступ Нікова",
              "date": "2026-11-04T19:00:00Z",
              "price": "550.00"
            },
            {
              "id": 36,
              "title": "Молодіжний музичний марафон",
              "date": "2026-11-28T16:00:00Z",
              "price": "450.00"
            }
          ]
        },
        "venue": {
          "id": 5,
          "name": "Bel Etage",
          "description": "Затишний концертний зал у центрі міста.",
          "city": "Київ",
          "address": "вул. Шота Руставелі, 16а",
          "events": [
            {
              "id": 3,
              "title": "Чуттєвий виступ Нікова",
              "date": "2026-11-04T19:00:00Z",
              "price": "550.00"
            },
            {
              "id": 10,
              "title": "Акустичний концерт Wellboy",
              "date": "2026-11-21T19:00:00Z",
              "price": "600.00"
            },
            {
              "id": 20,
              "title": "Вечірній живий стендап",
              "date": "2026-11-27T19:00:00Z",
              "price": "400.00"
            },
            {
              "id": 24,
              "title": "Сучасна хореографічна вистава",
              "date": "2026-11-12T19:00:00Z",
              "price": "550.00"
            },
            {
              "id": 27,
              "title": "Поетичний вечір-вистава",
              "date": "2026-11-22T18:30:00Z",
              "price": "450.00"
            }
          ]
        }
      },
    ]
    ```

- **GET `/api/events/{id}`**
  - *Опис:* Отримати детальну інформацію про конкретну подію за її ID.
  - *Response Status:* 200 OK 
  - *Response Body:*
    ```json
    {
      "id": 1,
      "title": "Великий сольний концерт Океану Ельзи",
      "description": "Незабутнє шоу на головній арені країни з улюбленими хітами.",
      "price": "1200.00",
      "date": "2026-11-01T19:00:00Z",
      "category": {
        "id": 1,
        "name": "Концерти"
      },
      "artist": {
        "id": 12,
        "name": "Океан Ельзи",
        "description": "Головний рок-гурт країни на чолі з Святославом Вакарчуком.",
        "events": [
          {
            "id": 1,
            "title": "Великий сольний концерт Океану Ельзи",
            "date": "2026-11-01T19:00:00Z",
            "price": "1200.00"
          }
        ]
      },
      "venue": {
        "id": 1,
        "name": "Palace of Sports",
        "description": "Головна крита арена для масштабних концертів.",
        "city": "Київ",
        "address": "Спортивна площа, 1",
        "events": [
          {
            "id": 1,
            "title": "Великий сольний концерт Океану Ельзи",
            "date": "2026-11-01T19:00:00Z",
            "price": "1200.00"
          },
          {
            "id": 5,
            "title": "Масштабне шоу Дорофеєвої",
            "date": "2026-11-09T19:00:00Z",
            "price": "1100.00"
          },
          {
            "id": 51,
            "title": "Новий сольний концерт",
            "date": "2026-11-20T19:00:00Z",
            "price": "850.00"
          }
        ]
      }
    }
    ```

- **POST `/api/events`**
  - *Опис:* Додати нову подію.
  - *Request Body:*
    ```json
      {
        "title": "Новий сольний концерт",
        "description": "Презентація нового альбому",
        "price": 850.00,
        "date": "2026-11-20T19:00:00Z",
        "category_id": 1,
        "artist_id": 1,
        "venue_id": 1
      }
    ```
  - *Response Status:* 201 Created

- **PUT `/api/events/{id}`**
  - *Опис:* Оновити інформацію про подію.
  - *Request Body:* 
    ```json
    {
      "title": "сольний концерт",
      "description": "Презентація альбому",
      "price": 800.00,
      "date": "2026-11-20T19:00:00Z",
      "category_id": 1,
      "artist_id": 1,
      "venue_id": 1
    }
    ```
  - *Response Status:* 200 OK

- **DELETE `/api/events/{id}`**
  - *Опис:* Видалити подію.
  - *Response Status:* 204 No Content

---

### 📌 Endpoint: Артисти (Artists)
- **GET `/api/artists`** - отримати список усіх артистів. *(Status: 200 OK)*
- **GET `/api/artists/{id}`** - отримати деталі артиста та список його подій. *(Status: 200 OK)*
- **POST `/api/artists`** - додати нового артиста. *(Status: 201 Created)*
- **PUT `/api/artists/{id}`** - оновити дані артиста. *(Status: 200 OK)*
- **DELETE `/api/artists/{id}`** - видалити артиста. *(Status: 204 No Content)*

---

### 📌 Endpoint: Майданчики (Venues)
- **GET `/api/venues`** - отримати список усіх майданчиків. *(Status: 200 OK)*
- **GET `/api/venues/{id}`** - отримати деталі майданчика та події на ньому. *(Status: 200 OK)*
- **POST `/api/venues`** - додати новий майданчик. *(Status: 201 Created)*
- **PUT `/api/venues/{id}`** - оновити майданчик. *(Status: 200 OK)*
- **DELETE `/api/venues/{id}`** - видалити майданчик. *(Status: 204 No Content)*

---

### 📌 Endpoint: Реєстрація та авторизація (Auth)
- **POST `/api/auth/register`**
  - *Опис:* Реєстрація нового користувача з перевіркою валідації полів та збігу паролів.
  - *Request Body:* 
    ```json
    {
      "username": "viktoria",
      "first_name": "Вікторія",
      "email": "viktoria@example.com",
      "password": "Qwerty123!",
      "password_confirmation": "Qwerty123!"
    }
    ```
  - *Response Body:*
    ```json
    {
      "id": 4,
      "username": "viktoria",
      "first_name": "Вікторія",
      "last_name": "",
      "email": "viktoria@example.com"
    }
    ```
  - *Response Status:* 201 Created
- **POST `/api/auth/login`**
  - *Опис:* Авторизація користувача та отримання токенів.
  - *Request Body:* 
    ```json
    {
      "username": "viktoria",
      "password": "Qwerty123!"
    }
    ```
  - *Response Body:*
    ```json
    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc5Mzk5Mzk1NSwiaWF0IjoxNzkzOTA3NTU1LCJqdGkiOiI5NWQzZjAxNWM0OGU0Y2NiYjI4MjVmYmE3Y2Y3ZmJmMCIsInVzZXJfaWQiOjR9.3zP4X-P6EBlrXZQiJyrobKz3sKZ9_HP9on6FXxyA8Hg",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzOTExMTU1LCJpYXQiOjE3OTM5MDc1NTUsImp0aSI6ImI0MTJhYThiYzgxNTRhNTJiYjMxMjgzNjgwYzYyYjY3IiwidXNlcl9pZCI6NH0.nQEXJRo8xuY4D0cbrVzTrxNxSGgcgoIN7f_fxJ91_Hc"
    }
    ```
  - *Response Status:* 200 OK 
- **POST `api/auth/token/refresh`**
  - *Опис:* Оновлення `access`-токена за допомогою `refresh`-токена.
  - *Request Body:* 
    ```json
    {
      "refresh": "<ваш_refresh_токен>"
    }
    ```
  - *Response Body:*
    ```json
    {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzOTEyMTU5LCJpYXQiOjE3OTM5MDg1NTksImp0aSI6IjQ0ZWE5ZWQ2NGNlMjQ5NDdhMWU2OTA2Y2RmODg3OTI4IiwidXNlcl9pZCI6NH0.rDO8amDl267Zw4tHvDyhYiBDe7bR-5ajXwEC4l6On-Q"
    }
    ```
  - *Response Status:* 200 OK 

---

### 📌 Endpoint: Профіль (Users)
- **GET `/api/auth/users/{id}`**
  - *Опис:* Отримати профіль користувача за ID (вимагає авторизації).
  - *Headers:* `Authorization: Bearer <token>`
  - *Response Body:*
    ```json
    {
      "id": 4,
      "username": "viktoria",
      "first_name": "Вікторія",
      "last_name": "",
      "email": "viktoria@example.com"
    }
    ```
  - *Response Status:* 200 OK
- **PUT `/api/auth/users/{id}`**
  - *Опис:* Оновити дані профілю користувача (перевіряє, чи редагує користувач власний профіль).
  - *Headers:* `Authorization: Bearer <token>`
  - *Request Body:* 
    ```json
    {
      "username": "viktoria",
      "first_name": "Вікторія",
      "email": "vika@example.com",
      "password": "Qwerty123!",
      "password_confirmation": "Qwerty123!"
    }
    ```
  - *Response Body:*
    ```json
    {
      "id": 4,
      "username": "viktoria",
      "first_name": "Вікторія",
      "last_name": "",
      "email": "vika@example.com"
    }
    ```
  - *Response Status:* 200 OK

---

### 📌 Endpoint: Кошик (Cart)
- **GET `/api/cart`**
  - *Опис:* Переглянути товари (квитки), додані в кошик.
  - *Response Status:* 200 OK
- **POST `/api/cart`**
  - *Опис:* Додати квиток на подію в кошик.
  - *Request Body:* `{"user_id": 1, "event_id": 1, "amount": 2}`
  - *Response Status:* 201 Created
- **DELETE `/api/cart/{id}`**
  - *Опис:* Видалити позицію з кошика.
  - *Response Status:* 204 No Content

---

### 📌 Endpoint: Замовлення (Orders)
- **POST `/api/orders`**
  - *Опис:* Створити замовлення на основі кошика.
  - *Response Status:* 201 Created
- **GET `/api/orders`**
  - *Опис:* Переглянути історію замовлень авторизованого користувача.
  - *Response Status:* 200 OK

---

## 🛡️ Права доступу (Permissions)

У проєкті реалізовано надійне розмежування прав:
- **Публічні ендпоінти (`AllowAny`)**: Перегляд списків подій, артистів та майданчиків доступний усім користувачам (гостям).
- **Адміністративні ендпоінти (`IsAdminUser`)**: Операції створення (POST), редагування (PUT) та видалення (DELETE) ресурсів дозволені виключно адміністраторам.
- **Захищені ендпоінти (`IsAuthenticated / перевірка власності`)**: Доступ до профілю та його редагування вимагають дійсного JWT-токена та перевірки на відповідність користувача.
- **Статуси помилок доступу:**
  - `401 Unauthorized` - токен відсутній або протух.
  - `403 Forbidden` - недостатньо прав (ролі) для виконання дії або спроба редагування чужого профілю.

## 🗃️ Схема бази даних

![Схема бази даних](images/db_scheme.jpg)

---

## 🚀 Як запустити проєкт

Щоб розгорнути та запустити бекенд-частину проєкту локально на комп'ютері, виконайте такі кроки:

### 1. Клонування репозиторію
Склонуйте репозиторій через термінал:
```bash
git clone <посилання-на-репозиторій>
```

### 2. Створення та активація віртуального середовища

Створіть віртуальне середовище Python та активуйте його:

- **Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

- **macOS / Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Встановлення залежностей

Встановіть усі необхідні бібліотеки з файлу `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Запуск міграцій бази даних

Створіть структуру бази даних за допомогою міграцій Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Запуск локального сервера

Запустіть сервер для розробки:

```bash
python manage.py runserver
```

Після цього бекенд буде доступний за адресою: `http://127.0.0.1:8000/`
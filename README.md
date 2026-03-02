# Broker Backend (Django + API)

Backend for a brokerage / investment platform built with **Django** and **Django REST Framework**.
The project provides both a web interface and API endpoints for managing users, wallets, and investments.

---

# Features

### Web Application

* User signup and login
* User dashboard
* Wallet system
* Transactions
* Investment tracking
* Profile management
* Admin management panel

### API

* Authentication endpoints
* User data access
* Wallet information
* Transactions API
* Investment API

---

# Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* HTML / CSS / JavaScript
* Gunicorn
* Whitenoise
* Render (deployment)

---

# Project Structure

```
broker-backend/
│
├── BrokerApp/
│   ├── models.py
│   ├── views.py
│   ├── api_views.py
│   ├── serializers.py
│   ├── urls.py
│
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

---

# Installation

Clone the repository

```
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run migrations

```
python manage.py migrate
```

Create admin user

```
python manage.py createsuperuser
```

Run the development server

```
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000
```

---

# API Endpoints

Example endpoints:

```
/api/login/
/api/register/
/api/dashboard/
/api/transactions/
/api/investments/
```

API responses are returned in **JSON format**.

---

# Environment Variables

Create a `.env` file:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
```

---

# Deployment (Render)

Build command

```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command

```
gunicorn broker.wsgi
```

---

# Author

Stephen Onyekachi

---

# Future Improvements

* Mobile app integration
* Payment gateway
* WebSocket notifications
* More API endpoints

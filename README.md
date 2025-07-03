# 🔐 Secure File Sharing Platform (Django)

A secure, role-based file sharing platform built with Django. It enables two types of users to interact securely through a document exchange system.

---

## 👥 User Roles

### 1. OPS Users
- Register and log in
- Upload files (`.docx`, `.pptx`, `.xlsx`)
- Email verification required before login

### 2. Client Users
- Register and log in
- Verify email via secure token
- Securely download files uploaded by OPS users
- Download click count is tracked
- Access is restricted to verified users only

---

## 🚀 Features
- Role-based authentication and dashboards
- Email verification for both OPS and Clients
- Secure download links using UUID tokens
- Session-based authentication
- Clean Bootstrap-styled UI
- File type validation and access control
- Download count tracking
- Real-time SMTP email notifications

---

## ⚙️ Tech Stack
- Python 3.x
- Django 5.x
- Django REST Framework
- SQLite (default) or PostgreSQL
- Bootstrap 5
- Gmail SMTP for email verification

---

## 📁 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If `requirements.txt` is missing, manually install:
```bash
pip install django djangorestframework python-dotenv
```

---

## 🔐 4. Environment Variables (`.env` file)

Create a `.env` file in the project root:

```
# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Default sender
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

> 🧠 Use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if using Gmail with 2FA.

---

## 🗃️ 5. Database Setup

### Default: SQLite  
No changes needed. Django uses `db.sqlite3`.

**Or**, for PostgreSQL/MySQL, update `settings.py > DATABASES`.

---

## 🔧 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## ▶️ 8. Run Development Server

```bash
python manage.py runserver
```

Then visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 9. Testing APIs with Postman

You can test:

| Endpoint                     | Method | Access  | Description                              |
|-----------------------------|--------|---------|------------------------------------------|
| `/api/signup/`              | POST   | Public  | Register Client                          |
| `/api/signup-ops/`          | POST   | Public  | Register OPS                             |
| `/api/verify-email/<uid>/<token>/` | GET    | Public  | Email verification                       |
| `/api/login/`               | POST   | Public  | Login (Client)                           |
| `/api/login-ops/`           | POST   | Public  | Login (OPS)                              |
| `/api/upload/`              | POST   | OPS     | Upload file                              |
| `/api/files/`               | GET    | Client  | List files                               |
| `/api/get-uuid-download-link/<id>/` | GET | Client | Get secure download link                |
| `/api/download-by-token/<uuid>/`    | GET | Client | Download file via secure token          |

---

## 📌 Folder Structure Overview

```
file_share_project/
├── file_share_project/        # Django settings
│   └── settings.py
├── fileshare/                 # App with models/views/urls
├── home/                      # Frontend + login/register views
├── templates/                 # HTML files
├── media/uploads/             # Uploaded files
├── db.sqlite3                 # SQLite DB
├── .env                       # Email credentials
└── .gitignore
```

---

## 🧹 .gitignore (Sample)

```
# Python
__pycache__/
*.py[cod]

# Env & DB
.env
env/
db.sqlite3

# Uploads & Migrations
/media/uploads/
**/migrations/*.py
**/migrations/__pycache__/

# IDE
.vscode/
.idea/
```

---

## ✉️ Email Template (Optional)

Add `templates/email_verification.html` for HTML-based emails.

---

## 🛠️ Optional Improvements

- Use JWT authentication
- Add rate-limiting or CAPTCHA
- Setup PostgreSQL for production
- Deploy with Docker/Gunicorn/NGINX
- Implement logging & audit trail

---

## 🚀 Deployment Strategy (Production Environment)

To securely deploy this Django project to a production environment, the following best practices are recommended:

---

### 🌐 1. Use a Production Web Server

- Replace `runserver` (development only) with **Gunicorn** or **uWSGI** as the WSGI server.
- Use **NGINX** as a reverse proxy to serve static files and route requests to Gunicorn.

```bash
# Example: install Gunicorn
pip install gunicorn
gunicorn file_share_project.wsgi
```

---

### 🛡️ 2. Secure Secrets and Environment

- Do **not** commit `.env` to version control.
- Use environment variables for production secrets like:
  - `SECRET_KEY`
  - `EMAIL_HOST_USER`
  - `EMAIL_HOST_PASSWORD`
- Use a service like **AWS Secrets Manager**, **Azure Key Vault**, or **Django-environ** for security.

---

### 🗃️ 3. Use PostgreSQL Instead of SQLite

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

> Use managed DBs like **Amazon RDS**, **Heroku Postgres**, or **DigitalOcean Managed DBs** in production.

---

### 📦 4. Optional: Use Docker

Package the app with Docker for consistent deployment across environments.

- `Dockerfile` for Python/Django app
- `docker-compose.yml` for DB + app setup
- Use `.env` for secrets and configs

Example:

```bash
docker-compose up --build
```

---

### ☁️ 5. Deploy to a Cloud Platform

Options include:

- **Heroku** (Quickest for beginners)
- **Render** or **Railway**
- **DigitalOcean App Platform**
- **AWS EC2 + RDS**
- **Azure App Services**
- **GCP App Engine**

---

### 🧩 6. Static and Media File Handling

- Use `collectstatic` to gather static files:
  ```bash
  python manage.py collectstatic
  ```
- Serve media uploads via:
  - AWS S3 (using `django-storages`)
  - NGINX static path
  - Custom CDN

---

### 🔐 7. HTTPS & Domain Setup

- Use **Let’s Encrypt** with **Certbot** for SSL.
- Configure NGINX or your cloud provider to redirect all HTTP to HTTPS.
- Add a custom domain and configure DNS records.

---

### ✅ Summary

| Component            | Recommended Tool        |
|---------------------|-------------------------|
| Web Server          | NGINX + Gunicorn        |
| Database            | PostgreSQL              |
| Static/Media Files  | S3 or NGINX             |
| Email               | Gmail SMTP / Mailgun    |
| HTTPS               | Let's Encrypt / Cloudflare |
| Secrets             | `.env` or Secret Manager |
| Containerization    | Docker (optional)       |
| Platform            | Heroku / Render / AWS   |

---


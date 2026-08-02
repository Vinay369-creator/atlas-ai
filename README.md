# Atlas AI – Intelligent Telegram Assistant

A production-quality AI-powered Telegram assistant that acts as a smart personal assistant for finance intelligence, news updates, and conversational AI.

## 🎯 Features

### Core Features
- **Conversational Onboarding**: Natural user profile creation with interests, industries, and preferences
- **User Personalization**: Stores and remembers user preferences and conversation history
- **Finance Intelligence**: Live financial news fetching, summarization, and insights
- **Daily Briefings**: Scheduled morning, evening, and weekly updates
- **AI Conversations**: Natural language interactions with context awareness
- **Live Information**: Real-time data from public APIs
- **Telegram Integration**: Rich messages, inline keyboards, and interactive responses
- **Integrations**: Gmail and Google Calendar integration (optional)

## 🏗️ Tech Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Language**: Python 3.10+
- **Database**: SQLite3 (Production-ready)
- **Message Queue**: Celery + Redis
- **Task Scheduler**: APScheduler / Celery Beat
- **LLM API**: OpenAI GPT-4
- **Telegram**: python-telegram-bot
- **APIs**: NewsAPI, Alpha Vantage, Google APIs

## 📁 Project Structure

```
atlas_ai/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── db.sqlite3
├── logs/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── celery.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       └── production.py
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   ├── admin.py
│   ├── migrations/
│   └── __init__.py
├── telegram_bot/
│   ├── handlers.py
│   ├── commands.py
│   ├── callbacks.py
│   ├── utils.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   ├── middleware.py
│   ├── admin.py
│   └── __init__.py
├── chat/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── __init__.py
├── finance/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── urls.py
│   ├── admin.py
│   ├── apis/
│   │   ├── __init__.py
│   │   ├── news_api.py
│   │   ├── stock_api.py
│   │   └── crypto_api.py
│   ├── migrations/
│   └── __init__.py
├── ai/
│   ├── __init__.py
│   ├── llm_client.py
│   ├── prompt_manager.py
│   ├── response_formatter.py
│   └── services.py
├── integrations/
│   ├── __init__.py
│   ├── gmail/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── services.py
│   ├── google_calendar/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── services.py
│   └── auth.py
├── scheduler/
│   ├── __init__.py
│   ├── tasks.py
│   ├── jobs.py
│   └── services.py
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── __init__.py
├── core/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── utils.py
│   ├── logger.py
│   ├── constants.py
│   └── decorators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_telegram_bot.py
│   ├── test_ai_services.py
│   └── test_finance_services.py
└── scripts/
    ├── __init__.py
    ├── init_db.py
    └── setup.sh
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Redis server
- OpenAI API Key
- Telegram Bot Token
- NewsAPI Key (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Vinay369-creator/atlas-ai.git
cd atlas-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Initialize database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Start Redis**
```bash
redis-server
```

7. **Run Celery worker** (in another terminal)
```bash
celery -A config worker -l info
```

8. **Run Celery beat** (in another terminal)
```bash
celery -A config beat -l info
```

9. **Start development server**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📋 Database Models

### accounts/
- **User**: Core user model with Telegram ID
- **UserProfile**: Extended user preferences and interests
- **UserPreferences**: Notification and briefing settings

### chat/
- **Conversation**: Message history and context
- **Message**: Individual messages in conversations

### finance/
- **NewsCache**: Cached financial news
- **Stock**: Stock information cache
- **MarketInsight**: Market insights and analysis

### notifications/
- **NotificationLog**: Tracking sent notifications
- **ScheduledBriefing**: Scheduled briefing configuration

## 🤖 Telegram Commands

```
/start - Onboarding and initialization
/help - Help and available commands
/brief - Get instant briefing
/add_interest - Add new interests
/settings - Manage preferences
/news - Get latest financial news
/insights - Get market insights
/about - About the assistant
/portfolio - View tracked portfolio
/alerts - Manage price alerts
```

## 🔧 API Endpoints

### Admin
- `/admin/` - Django admin panel

### Chat
- `POST /api/chat/message/` - Send message to AI
- `GET /api/chat/history/` - Get conversation history
- `DELETE /api/chat/history/{id}/` - Delete message

### Finance
- `GET /api/finance/news/` - Get financial news
- `GET /api/finance/briefing/` - Get briefing
- `GET /api/finance/stock/{symbol}/` - Get stock info
- `POST /api/finance/alerts/` - Create price alert

### User
- `GET /api/user/profile/` - Get user profile
- `PUT /api/user/profile/` - Update profile
- `PUT /api/user/preferences/` - Update preferences
- `POST /api/user/interests/` - Add interests

### Telegram Webhook
- `POST /api/telegram/webhook/` - Telegram webhook endpoint

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_finance_services.py

# Run with verbose output
pytest -v
```

## 📦 Deployment

### Production Setup

1. **Update environment variables**
```bash
DEBUG=False
SECRET_KEY=your-secure-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ENVIRONMENT=production
```

2. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

3. **Run migrations**
```bash
python manage.py migrate --run-syncdb
```

4. **Start with Gunicorn**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

5. **Setup Nginx reverse proxy** (recommended)

## 🔐 Security

- Environment variables for sensitive data
- CSRF protection enabled
- Rate limiting implemented
- Input validation and sanitization
- Secure token storage with encryption
- OAuth 2.0 for integrations
- HTTPS required in production
- SQL injection protection via ORM

## 📝 License

MIT License - See LICENSE file

## 👨‍💻 Author

Vinay369-creator

## 📞 Support

For issues and questions, please open an issue on GitHub.

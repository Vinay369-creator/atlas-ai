# Atlas AI - Financial Intelligence Assistant

## Overview

Atlas AI is an intelligent financial assistant powered by OpenAI's GPT-4 and integrated with Telegram for seamless access to financial news, market insights, and investment information.

## Features

- 🤖 **AI-Powered Conversations**: Get intelligent financial insights via OpenAI's GPT-4
- 📱 **Telegram Integration**: Access Atlas AI directly from Telegram
- 📰 **Financial News**: Stay updated with latest market news and trends
- 📊 **Market Insights**: Detailed analysis of stocks, sectors, and markets
- 🎯 **Personalized Briefings**: Daily customized financial briefings
- 💰 **Price Alerts**: Track stock prices and get notified on price changes
- 🔔 **Smart Notifications**: Relevant alerts based on your interests
- ⚙️ **Customizable Preferences**: Tailor the experience to your needs

## Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery + Celery Beat
- **WebSocket**: Django Channels
- **API Documentation**: drf-spectacular (OpenAPI 3.0)

### AI & Integration
- **LLM**: OpenAI GPT-4
- **Telegram Bot**: python-telegram-bot
- **Async Support**: Daphne ASGI server

### DevOps
- **Containerization**: Docker & Docker Compose
- **Process Manager**: Gunicorn + Nginx
- **Code Quality**: Black, Flake8, isort
- **Testing**: pytest + pytest-django

## Project Structure

```
atlas-ai/
├── project/                 # Django project configuration
│   ├── settings.py         # Main settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI application
│   ├── asgi.py             # ASGI application
│   └── celery.py           # Celery configuration
├── accounts/               # User accounts & profiles
│   ├── models.py           # User, Profile, Interests, Companies
│   ├── services.py         # User services
│   └── serializers.py      # API serializers
├── ai/                     # AI & LLM services
│   ├── llm_client.py       # OpenAI API client
│   ├── prompt_manager.py   # Prompt generation
│   ├── response_formatter.py # Response formatting
│   └── services.py         # AI service layer
├── chat/                   # Chat & conversation management
│   ├── models.py           # Conversation, Message models
│   ├── services.py         # Chat services
│   └── serializers.py      # API serializers
├── telegram_bot/           # Telegram bot handlers
│   ├── handlers/           # Command & message handlers
│   ├── bot.py              # Bot setup & configuration
│   └── management/         # Management commands
├── api/                    # REST API endpoints
│   ├── views.py            # API views
│   ├── urls.py             # API routing
│   └── permissions.py      # Custom permissions
├── core/                   # Core utilities
│   ├── constants.py        # Application constants
│   ├── exceptions.py       # Custom exceptions
│   ├── middleware.py       # Django middleware
│   ├── decorators.py       # Utility decorators
│   └── views.py            # Base views
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Docker & Docker Compose (optional)

### Setup

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

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=atlas_ai
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/1

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2048

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Running Services

### Development

1. **Django Development Server**
   ```bash
   python manage.py runserver
   ```

2. **Telegram Bot**
   ```bash
   python manage.py start_bot
   ```

3. **Celery Worker**
   ```bash
   celery -A project worker -l info
   ```

4. **Celery Beat (Scheduler)**
   ```bash
   celery -A project beat -l info
   ```

### Production with Docker

```bash
docker-compose up -d
```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Telegram Bot Commands

- `/start` - Start using Atlas AI
- `/help` - Show available commands
- `/brief` - Get daily briefing
- `/news` - Get latest financial news
- `/insights` - Get market insights
- `/settings` - Manage preferences
- `/add_interest` - Add interest topics
- `/add_company` - Add companies to follow
- `/about` - About Atlas AI

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/logout/` - Logout
- `POST /api/v1/auth/register/` - Register

### Conversations
- `GET /api/v1/conversations/` - List conversations
- `POST /api/v1/conversations/` - Create conversation
- `GET /api/v1/conversations/{id}/` - Get conversation
- `POST /api/v1/conversations/{id}/messages/` - Add message

### User Preferences
- `GET /api/v1/profile/` - Get user profile
- `PUT /api/v1/profile/` - Update profile
- `GET /api/v1/interests/` - Get interests
- `POST /api/v1/interests/` - Add interest

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_ai_service.py
```

## Logging

Logs are stored in the `logs/` directory:
- `atlas_ai.log` - Main application log

Log levels can be configured in `project/settings.py`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Quality

```bash
# Format code with Black
black .

# Check code style
flake8 .

# Sort imports
isort .
```

## License

MIT License - See LICENSE file for details

## Support

For support, email support@atlasai.com or open an issue on GitHub.

## Acknowledgments

- OpenAI for GPT-4 API
- Telegram for Bot API
- Django community

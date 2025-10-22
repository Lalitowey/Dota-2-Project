# Dota 2 Analytics

<div align="center">

**Full-stack Dota 2 analytics web application with FastAPI backend and Nuxt 3 frontend**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Nuxt](https://img.shields.io/badge/Nuxt-3.17+-00DC82.svg)](https://nuxt.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development](#development)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Dota 2 Analytics is a comprehensive web application for analyzing Dota 2 player statistics, hero data, and match history. The application provides real-time data visualization, player search, and detailed performance metrics by integrating with the OpenDota API.

## ✨ Features

- **Player Analytics**
  - Player profile and statistics
  - Win/loss records and trends
  - Hero performance analysis
  - Match history with detailed breakdowns
  
- **Hero Database**
  - Complete hero constants and metadata
  - Hero statistics and pick/win rates
  - Item builds and recommendations
  
- **Performance**
  - Intelligent caching system with TTL
  - Optimized API proxy architecture
  - Real-time data updates
  
- **Modern UI/UX**
  - Responsive design with Tailwind CSS v4
  - Dark mode support
  - Interactive data tables with sorting/filtering
  - Beautiful data visualizations

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Nuxt 3        │ ◄─────► │   FastAPI        │ ◄─────► │   OpenDota      │
│   Frontend      │  HTTP   │   Backend        │  HTTP   │   API           │
│   (Port 3000)   │         │   (Port 8000)    │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   PostgreSQL     │
                            │   Database       │
                            │   (Port 5432)    │
                            └──────────────────┘
```

### Backend (FastAPI)
- RESTful API proxy for OpenDota
- In-memory caching with configurable TTL
- CORS-enabled for frontend integration
- Comprehensive error handling and logging
- Modular architecture with clean separation of concerns

### Frontend (Nuxt 3)
- Server-side rendering (SSR) capable
- Type-safe with TypeScript
- State management with Pinia
- shadcn-vue UI components
- Tailwind CSS v4 for styling

### Database (PostgreSQL)
- Persistent data storage
- User preferences and settings
- Cache optimization (future implementation)

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.10+
- **HTTP Client**: httpx
- **Database ORM**: SQLAlchemy 2.0
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Code Quality**: black, ruff, mypy

### Frontend
- **Framework**: Nuxt 3.17+
- **Language**: TypeScript 5+
- **UI Library**: shadcn-vue with reka-ui
- **Styling**: Tailwind CSS v4
- **State Management**: Pinia
- **Data Tables**: @tanstack/vue-table
- **Package Manager**: Bun

### Infrastructure
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn (backend), Node (frontend dev)

## 📦 Prerequisites

- **Python**: 3.10 or higher
- **Bun**: Latest version (for frontend)
- **PostgreSQL**: 15+ (or use Docker)
- **Docker & Docker Compose**: Latest (optional, for containerized setup)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd Dota-2-Project

# Start all services
docker-compose up --build
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### Option 2: Local Development

#### Backend Setup

```bash
# Navigate to project root
cd Dota-2-Project

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Start PostgreSQL (or use Docker)
docker run -d \
  --name dota-postgres \
  -e POSTGRES_USER=dota_user \
  -e POSTGRES_PASSWORD=dota_password \
  -e POSTGRES_DB=dota_db \
  -p 5432:5432 \
  postgres:15-alpine

# Run backend server
cd backend
uvicorn app.main_new:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend/dota-2-project

# Install dependencies with Bun
bun install

# Start development server
bun run dev
```

## 💻 Development

### Backend Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Run development server with auto-reload
cd backend
uvicorn app.main_new:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

### Frontend Development

```bash
cd frontend/dota-2-project

# Development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview

# Generate static site
bun run generate

# Type checking
bun run typecheck

# Linting
bun run lint
```

## 🧪 Testing

### Backend Tests

The backend includes a comprehensive test suite with 42+ tests covering:

- Main application endpoints
- Configuration management
- Cache operations
- HTTP client functionality
- All API endpoints (players, heroes, cache)

```bash
cd backend

# Run all tests
pytest

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run with coverage report
pytest --cov=app --cov-report=term-missing --cov-report=html

# View coverage report
open htmlcov/index.html
```

For detailed testing documentation, see [backend/tests/README.md](backend/tests/README.md).

## 📁 Project Structure

```
Dota-2-Project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── players.py      # Player endpoints
│   │   │       │   ├── heroes.py       # Hero endpoints
│   │   │       │   ├── matches.py      # Match endpoints
│   │   │       │   └── cache.py        # Cache management
│   │   │       └── router.py           # API router aggregation
│   │   ├── core/
│   │   │   ├── client.py               # OpenDota HTTP client
│   │   │   └── cache.py                # Cache implementation
│   │   ├── config.py                   # Configuration management
│   │   └── main_new.py                 # FastAPI application
│   ├── tests/                          # Test suite (42+ tests)
│   │   ├── conftest.py                 # Test fixtures
│   │   ├── test_main.py
│   │   ├── test_config.py
│   │   ├── test_cache.py
│   │   ├── test_client.py
│   │   ├── test_api_players.py
│   │   ├── test_api_heroes.py
│   │   └── test_api_cache.py
│   ├── requirements.txt                # Python dependencies
│   ├── pytest.ini                      # Pytest configuration
│   └── Dockerfile
├── frontend/
│   └── dota-2-project/
│       ├── components/
│       │   └── ui/                     # shadcn-vue components
│       ├── pages/
│       │   └── index.vue               # Main dashboard
│       ├── stores/
│       │   └── heroStore.ts            # Pinia store for heroes
│       ├── plugins/
│       │   └── loadHeroConstants.ts    # Hero data initialization
│       ├── nuxt.config.ts              # Nuxt configuration
│       ├── tailwind.config.js          # Tailwind configuration
│       ├── package.json
│       ├── bun.lock
│       └── Dockerfile
├── docker-compose.yml                  # Multi-service orchestration
├── .env                                # Environment variables
├── .gitignore
├── WARP.md                            # AI assistant context
└── README.md
```

## 📚 API Documentation

### Base URL
- **Local**: `http://localhost:8000`
- **API Prefix**: `/api/v1/opendota_proxy`

### Available Endpoints

#### Player Endpoints
- `GET /players/{account_id}` - Get player profile
- `GET /players/{account_id}/wl` - Get win/loss statistics
- `GET /players/{account_id}/totals` - Get performance totals
- `GET /players/{account_id}/heroes` - Get player hero statistics
- `GET /players/{account_id}/matches` - Get match history
- `GET /search?q={query}` - Search for players

#### Hero Endpoints
- `GET /constants/heroes` - Get hero constants
- `GET /heroStats` - Get hero statistics
- `GET /constants/items` - Get item constants

#### Cache Management
- `GET /cache/stats` - Get cache statistics
- `DELETE /cache/clear` - Clear all cache

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
# Backend Configuration
APP_NAME="Dota 2 Analytics API"
APP_VERSION="1.0.0"
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://dota_user:dota_password@localhost:5432/dota_db

# OpenDota API
OPENDOTA_API_KEY=your_api_key_here  # Optional
OPENDOTA_BASE_URL=https://api.opendota.com/api

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Cache TTL (in minutes)
CACHE_TTL_HERO_CONSTANTS=1440
CACHE_TTL_PLAYER_PROFILE=30
CACHE_TTL_PLAYER_WINLOSS=60
CACHE_TTL_PLAYER_HEROES=120
CACHE_TTL_PLAYER_MATCHES=10
CACHE_TTL_SEARCH_RESULTS=5

# Frontend Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000

# GitHub (optional)
GITHUB_TOKEN=your_github_token_here
```

## 🐳 Docker Deployment

### Production Build

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v
```

### Individual Services

```bash
# Start only database
docker-compose up db -d

# Start backend (requires database)
docker-compose up backend -d

# Start frontend (requires backend)
docker-compose up frontend -d
```

### Service Access

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Database**: localhost:5432
  - User: `dota_user`
  - Password: `dota_password`
  - Database: `dota_db`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards

**Backend**:
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all public methods
- Maintain test coverage above 80%
- Run `black`, `ruff`, and `mypy` before committing

**Frontend**:
- Follow Vue.js style guide
- Use TypeScript for type safety
- Write component documentation
- Test components before committing

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenDota API](https://docs.opendota.com/) - Dota 2 data provider
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Nuxt 3](https://nuxt.com/) - Vue.js framework
- [shadcn-vue](https://www.shadcn-vue.com/) - UI component library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

## 📞 Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Check existing documentation in `WARP.md`
- Review API documentation at `/docs`

---

<div align="center">

Made with ❤️ for the Dota 2 community

</div>
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Dota 2 analytics web application built as a full-stack solution with a FastAPI backend that proxies OpenDota API requests and a Nuxt 3 frontend for data visualization and user interaction.

## Architecture

### Backend (`/backend`)
- **Framework**: FastAPI with Python 3.10
- **Purpose**: API proxy to OpenDota, handles CORS, serves player/hero data
- **Key Dependencies**: fastapi, uvicorn, httpx
- **Main File**: `backend/app/main.py` - Contains all API endpoints

### Frontend (`/frontend/dota-2-project`)
- **Framework**: Nuxt 3 with TypeScript
- **UI Components**: shadcn-vue with Tailwind CSS v4
- **State Management**: Pinia stores
- **Key Dependencies**: Vue 3, Nuxt 3, @tanstack/vue-table, reka-ui

### Database
- **Type**: PostgreSQL 15 (via Docker)
- **Configuration**: docker-compose.yml defines database service
- **Credentials**: dota_user/dota_password/dota_db

## Development Commands

### Full Stack Development (Docker)
```bash
# Start all services (backend, frontend, database)
docker-compose up --build

# Start services in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Reset database
docker-compose down -v && docker-compose up --build
```

### Backend Development
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run development server (manual)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
cd backend && python -m pytest

# Deactivate virtual environment
deactivate
```

### Frontend Development
```bash
# Navigate to frontend project
cd frontend/dota-2-project

# Install dependencies
npm install
# or with bun (project uses bun.lock)
bun install

# Development server
npm run dev
# or
bun run dev

# Build for production
npm run build
bun run build

# Preview production build
npm run preview
bun run preview

# Generate static site
npm run generate
bun run generate
```

## Key Architecture Components

### Backend API Endpoints
All endpoints are prefixed with `/api/v1/opendota_proxy/`:
- `GET /players/{account_id}` - Player profile data
- `GET /players/{account_id}/wl` - Win/loss statistics
- `GET /players/{account_id}/totals` - Player performance totals
- `GET /players/{account_id}/heroes` - Player hero statistics
- `GET /constants/heroes` - Hero constants/metadata
- `GET /search?q={query}` - Player search

### Frontend State Management
- **Hero Store** (`stores/heroStore.ts`): Manages hero constants and metadata
- **Pinia Plugin** (`plugins/loadHeroConstants.ts`): Loads hero data on app initialization

### Frontend Routing Structure
- `/` - Main dashboard (pages/index.vue)
- `/heroes` - Hero analytics
- `/players` - Player search and analytics
- Components organized in `components/ui/` for reusable shadcn-vue elements

### Configuration Files
- `nuxt.config.ts` - Nuxt configuration with Tailwind, shadcn, Pinia
- `docker-compose.yml` - Multi-service orchestration
- `.env` - Environment variables (contains API keys)
- `backend/requirements.txt` - Python dependencies

## Environment Variables

### Frontend Runtime Config
- `NUXT_PUBLIC_API_BASE_URL` - Backend API URL (defaults to http://localhost:8000)

### Environment File (.env)
Contains GitHub and OpenDota API credentials - never commit real values.

## Development Workflow

### Single Service Development
1. **Backend Only**: Use `source .venv/bin/activate && cd backend && uvicorn app.main:app --reload`
2. **Frontend Only**: Use `cd frontend/dota-2-project && npm run dev`
3. **Database Only**: Use `docker-compose up db -d`

### Code Organization Patterns
- Backend follows FastAPI conventions with all routes in `main.py`
- Frontend uses Nuxt 3 auto-imports and file-based routing
- State management centralized in Pinia stores
- UI components follow shadcn-vue patterns with TypeScript interfaces
- Hero data loaded globally via Nuxt plugin system

### OpenDota API Integration
The backend serves as a CORS-enabled proxy to OpenDota's public API, handling:
- Player profile and statistics retrieval
- Hero constants and metadata
- Player search functionality
- Error handling and logging for API requests

All OpenDota requests go through the backend proxy to avoid CORS issues and centralize API key management.
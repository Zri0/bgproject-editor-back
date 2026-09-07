# Card Editor - Backend (Django)

REST API for creating and editing game cards with buffs and effects.

## Stack

- **Framework**: Django 5.0 (LTS)
- **API**: Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **CORS**: django-cors-headers
- **Environment**: python-decouple

## Installation

### Prerequisites
- Python 3.10+
- pip

### Installation steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/card-editor-backend.git
   cd card-editor-backend
   ```

2. **Create and activate a virtual environment**
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
   # Edit .env with your values
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for Django Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial configuration**
   ```bash
   python manage.py load_config
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000/api/`

## API Endpoints

### Cards
- `GET /api/cards/` - List all cards
- `POST /api/cards/` - Create a new card
- `GET /api/cards/{id}/` - Get card detail
- `PUT /api/cards/{id}/` - Update a card
- `DELETE /api/cards/{id}/` - Delete a card
- `POST /api/cards/{id}/add-buff/` - Add buff to card
- `DELETE /api/cards/{id}/remove-buff/{buff_id}/` - Remove buff
- `POST /api/cards/{id}/add-effect/` - Add effect to card
- `DELETE /api/cards/{id}/remove-effect/{effect_id}/` - Remove effect

### Buffs
- `GET /api/buffs/` - List all buffs
- `GET /api/buffs/{id}/` - Get buff detail

### Effects
- `GET /api/effects/` - List all effects
- `GET /api/effects/{id}/` - Get effect detail

## Data Model

### Buff
```json
{
  "id": 1,
  "name": "HealthBoost",
  "description": "Increases health",
  "attributes": [
    {"name": "hp", "type": "integer"},
    {"name": "regen", "type": "integer"}
  ]
}
```

### Effect
```json
{
  "id": 1,
  "name": "Burn",
  "description": "Progressive burn damage",
  "attributes": [
    {"name": "damage", "type": "integer"},
    {"name": "duration", "type": "integer"}
  ]
}
```

### Card (creation)

The `image` field is an uploaded file stored and served by Django (not a URL).
Send the request as `multipart/form-data`:

```bash
curl -X POST http://localhost:8000/api/cards/ \
  -F "title=Fire Dragon" \
  -F "description=A pure fire dragon" \
  -F "image=@dragon.jpg" \
  -F "level=5" \
  -F "races=1" -F "races=2" \
  -F "attack=8" \
  -F "health=10"
```

Responses return `image` as an absolute URL (e.g. `http://localhost:8000/media/cards/dragon.jpg`),
or `null` when no image was uploaded. `image` is optional; on `PUT`/`PATCH` omit it to keep
the current file. Uploaded files live under `MEDIA_ROOT` (default `<BASE_DIR>/media/cards/`)
and are served at `/media/` while `DEBUG=True`.

## Adding Buffs/Effects to Cards

### Add Buff
```bash
POST /api/cards/1/add-buff/
{
  "buff": 1,
  "parameters": {"hp": 10, "regen": 2}
}
```

### Add Effect
```bash
POST /api/cards/1/add-effect/
{
  "effect": 1,
  "parameters": {"damage": 5, "duration": 3}
}
```

## Configuration

Configuration variables are loaded from `.env`:

- `AVAILABLE_LEVELS`: Available levels (e.g.: 1,2,3,4,5)
- `AVAILABLE_RACES`: Available races (e.g.: Human,Elf,Dwarf)
- `AVAILABLE_EFFECTS`: Effect names
- `AVAILABLE_BUFFS`: Buff names

**Note**: Effects and buffs must be configured with their attributes in Django Admin.

## Django Admin

Go to `http://localhost:8000/admin/` to manage:
- Cards
- Buffs (with their attributes)
- Effects (with their attributes)
- Buffs applied to cards
- Effects contained in cards

## Connecting with the Frontend

The Angular frontend should use the following environment variables:

```env
# environment.ts or environment.prod.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

Make sure `CORS_ALLOWED_ORIGINS` in `.env` includes the frontend URL:
```env
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

## Development

### Create migrations after changes to models
```bash
python manage.py makemigrations
python manage.py migrate
```

### Tests (once added)
```bash
python manage.py test
```

## Production

To deploy with Gunicorn:

```bash
gunicorn config.wsgi --bind 0.0.0.0:8000
```

Make sure to:
1. Set `DEBUG=False` in `.env`
2. Generate a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use PostgreSQL instead of SQLite
5. Configure `CORS_ALLOWED_ORIGINS` with the frontend's domain
6. Point `MEDIA_ROOT` at a persistent directory and have the web server (nginx/Apache)
   or an object storage backend serve `/media/` — Django does not serve it when `DEBUG=False`

## License

MIT

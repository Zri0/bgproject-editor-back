# Card Editor - Backend (Django)

API REST para crear y editar cartas de juego con buffs y efectos.

## Stack

- **Framework**: Django 5.0 (LTS)
- **API**: Django REST Framework
- **Database**: SQLite (desarrollo) / PostgreSQL (producción)
- **CORS**: django-cors-headers
- **Environment**: python-decouple

## Instalación

### Requisitos previos
- Python 3.10+
- pip

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/yourusername/card-editor-backend.git
   cd card-editor-backend
   ```

2. **Crear y activar virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus valores
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario (opcional, para Django Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Cargar configuración inicial**
   ```bash
   python manage.py load_config
   ```

8. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

El backend estará disponible en `http://localhost:8000/api/`

## API Endpoints

### Cartas
- `GET /api/cartas/` - Listar todas las cartas
- `POST /api/cartas/` - Crear una nueva carta
- `GET /api/cartas/{id}/` - Obtener detalle de una carta
- `PUT /api/cartas/{id}/` - Actualizar una carta
- `DELETE /api/cartas/{id}/` - Eliminar una carta
- `POST /api/cartas/{id}/add-buff/` - Agregar buff a carta
- `DELETE /api/cartas/{id}/remove-buff/{buff_id}/` - Remover buff
- `POST /api/cartas/{id}/add-efecto/` - Agregar efecto a carta
- `DELETE /api/cartas/{id}/remove-efecto/{efecto_id}/` - Remover efecto

### Buffs
- `GET /api/buffs/` - Listar todos los buffs
- `GET /api/buffs/{id}/` - Obtener detalle de un buff

### Efectos
- `GET /api/efectos/` - Listar todos los efectos
- `GET /api/efectos/{id}/` - Obtener detalle de un efecto

## Modelo de Datos

### Buff
```json
{
  "id": 1,
  "name": "HealthBoost",
  "description": "Aumenta la vida",
  "atributos": [
    {"nombre": "hp", "tipo": "entero"},
    {"nombre": "regen", "tipo": "entero"}
  ]
}
```

### Efecto
```json
{
  "id": 1,
  "name": "Burn",
  "description": "Quema progresiva",
  "atributos": [
    {"nombre": "damage", "tipo": "entero"},
    {"nombre": "duration", "tipo": "entero"}
  ]
}
```

### Carta (creación)
```json
{
  "titulo": "Fire Dragon",
  "descripcion": "Un dragón de fuego puro",
  "imagen": "https://example.com/images/dragon.jpg",
  "nivel": 5,
  "razas": ["Dragon", "Fire"],
  "ataque": 8,
  "vida": 10
}
```

## Agregar Buffs/Efectos a Cartas

### Agregar Buff
```bash
POST /api/cartas/1/add-buff/
{
  "buff": 1,
  "parametros": {"hp": 10, "regen": 2}
}
```

### Agregar Efecto
```bash
POST /api/cartas/1/add-efecto/
{
  "efecto": 1,
  "parametros": {"damage": 5, "duration": 3}
}
```

## Configuración

Las variables de configuración se cargan desde `.env`:

- `AVAILABLE_LEVELS`: Niveles disponibles (ej: 1,2,3,4,5)
- `AVAILABLE_RACES`: Razas disponibles (ej: Human,Elf,Dwarf)
- `AVAILABLE_EFFECTS`: Nombres de efectos
- `AVAILABLE_BUFFS`: Nombres de buffs

**Nota**: Los efectos y buffs deben ser configurados con sus atributos en Django Admin.

## Django Admin

Accede a `http://localhost:8000/admin/` para gestionar:
- Cartas
- Buffs (con sus atributos)
- Efectos (con sus atributos)
- Buffs aplicados a cartas
- Efectos contenidos en cartas

## Conexión con Frontend

El frontend Angular debe usar las siguientes variables de entorno:

```env
# environment.ts o environment.prod.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

Asegúrate de que `CORS_ALLOWED_ORIGINS` en `.env` incluya la URL del frontend:
```env
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

## Desarrollo

### Crear migraciones después de cambios en models
```bash
python manage.py makemigrations
python manage.py migrate
```

### Tests (cuando se agreguen)
```bash
python manage.py test
```

## Producción

Para desplegar con Gunicorn:

```bash
gunicorn config.wsgi --bind 0.0.0.0:8000
```

Asegúrate de:
1. Establecer `DEBUG=False` en `.env`
2. Generar una `SECRET_KEY` segura
3. Configurar `ALLOWED_HOSTS` con tu dominio
4. Usar PostgreSQL en lugar de SQLite
5. Configurar `CORS_ALLOWED_ORIGINS` con el dominio del frontend

## Licencia

MIT

# Finance Dashboard Backend

A FastAPI-based backend for a finance dashboard system with role-based access control, financial record management, and summary analytics.

## Overview

This backend implements a complete finance management system with the following key features:

- **User Management**: Create and manage users with different roles
- **Role-Based Access Control**: Three roles with distinct permissions (Viewer, Analyst, Admin)
- **Financial Records**: CRUD operations for income and expense transactions
- **Dashboard Analytics**: Summary data, category breakdowns, and monthly trends
- **Input Validation**: Comprehensive validation using Pydantic
- **Clean Architecture**: Separation of concerns with models, schemas, services, and routes

## Architecture

```
app/
├── main.py              # FastAPI application entry point
├── database.py          # SQLite database configuration
├── models/              # SQLAlchemy ORM models
│   ├── user.py
│   └── record.py
├── schemas/             # Pydantic validation schemas
│   ├── user.py
│   └── record.py
├── routes/              # API endpoints
│   ├── user_routes.py
│   ├── record_routes.py
│   └── dashboard_routes.py
├── services/            # Business logic layer
│   ├── user_service.py
│   └── record_service.py
├── core/                # Configuration and security
│   ├── config.py
│   └── security.py
└── utils/               # Utilities and dependencies
    └── dependencies.py
```

## Data Models

### User
- `id`: Unique identifier
- `username`: Unique username
- `email`: Unique email address
- `full_name`: User's full name
- `role`: User role (viewer, analyst, admin)
- `is_active`: Account status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Record
- `id`: Unique identifier
- `user_id`: Reference to user
- `amount`: Transaction amount (positive value)
- `type`: Transaction type (income/expense)
- `category`: Transaction category
- `date`: Transaction date
- `notes`: Optional notes/description
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Role-Based Access Control

### Viewer
- ✅ Read own financial records
- ✅ Access own dashboard summary
- ❌ Cannot create, update, or delete records
- ❌ Cannot manage users

### Analyst
- ✅ Create own financial records
- ✅ Read own records
- ✅ Update own records
- ✅ Delete own records
- ✅ Access own dashboard and analytics
- ✅ View category distribution and trends
- ❌ Cannot manage users

### Admin
- ✅ Full access to all operations
- ✅ Create and manage users
- ✅ Manage all financial records
- ✅ Access all dashboards
- ✅ Deactivate users

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. **Clone/Extract the project**
   ```bash
   cd finance-backend
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
# From the project root directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

This implementation uses **mock authentication** via HTTP headers for development purposes. In production, implement JWT tokens or OAuth2.

### How to Authenticate

Include the following headers in your requests:

```
X-User-Id: <user_id>
X-User-Role: <role>
```

Example:
```bash
curl -H "X-User-Id: 1" -H "X-User-Role: admin" http://localhost:8000/api/users
```

## API Endpoints

### Health Check
- `GET /` - Root health check
- `GET /health` - Health endpoint

### User Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/users/` | Create user | Admin |
| GET | `/api/users/{user_id}` | Get user details | Admin, Own User |
| GET | `/api/users/` | List all users | Admin |
| PUT | `/api/users/{user_id}` | Update user | Admin, Own User |
| DELETE | `/api/users/{user_id}` | Delete user | Admin |
| POST | `/api/users/{user_id}/deactivate` | Deactivate user | Admin |

### Financial Records

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/records/` | Create record | Analyst, Admin |
| GET | `/api/records/{record_id}` | Get record | Owner, Admin |
| GET | `/api/records/` | List user's records | All |
| PUT | `/api/records/{record_id}` | Update record | Owner, Admin |
| DELETE | `/api/records/{record_id}` | Delete record | Owner, Admin |

### Dashboard & Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/summary` | Get dashboard summary |
| GET | `/api/dashboard/categories` | Get category distribution |
| GET | `/api/dashboard/trends` | Get monthly trends |

## Request/Response Examples

### Create a User (Admin)
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "X-User-Id: 1" \
  -H "X-User-Role: admin" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "analyst"
  }'
```

### Create a Financial Record
```bash
curl -X POST "http://localhost:8000/api/records/" \
  -H "X-User-Id: 2" \
  -H "X-User-Role: analyst" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500.00,
    "type": "income",
    "category": "Salary",
    "date": "2024-01-15T10:00:00",
    "notes": "Monthly salary"
  }'
```

### Get Dashboard Summary
```bash
curl "http://localhost:8000/api/dashboard/summary" \
  -H "X-User-Id: 2" \
  -H "X-User-Role: analyst"
```

### List Records with Filters
```bash
curl "http://localhost:8000/api/records/?record_type=income&category=Salary" \
  -H "X-User-Id: 2" \
  -H "X-User-Role: analyst"
```

## Key Features

### 1. Input Validation
- All inputs validated using Pydantic schemas
- Email validation
- Amount must be positive
- Category and notes have length constraints
- Useful error messages with status codes

### 2. Error Handling
- Proper HTTP status codes (201, 400, 403, 404, etc.)
- Descriptive error messages
- Validation errors show specific field issues

### 3. Business Logic
- Automatic calculation of summaries (total income, expenses, balance)
- Category-wise aggregation
- Monthly trend analysis
- Recent activity tracking

### 4. Access Control
- Role-based middleware checks
- User isolation (can't access other users' data unless admin)
- Permission-based operation restrictions

### 5. Data Persistence
- SQLite database (file-based, no server required)
- SQLAlchemy ORM for type-safe queries
- Automatic timestamps (created_at, updated_at)
- Foreign key relationships

## Database

The application uses **SQLite** with file-based storage (`finance.db`).

### Initialize Database
The database is automatically initialized on application startup. Tables are created based on SQLAlchemy models.

### Database Location
```
finance-backend/finance.db
```

## Assumptions and Design Decisions

1. **Mock Authentication**: Uses header-based mock authentication for simplicity. In production, implement JWT or OAuth2.

2. **User Isolation**: Viewers, Analysts can only access their own data. Admins can access all data.

3. **Amount Storage**: Amounts stored as float. In production, use Decimal for financial precision.

4. **Timestamps**: All dates stored in UTC. Convert to user timezone on frontend.

5. **Soft Delete**: Not implemented for records. Full deletion used for simplicity.

6. **Rate Limiting**: Not implemented. Can be added with middleware.

7. **Pagination**: Implemented with skip/limit on list endpoints.

8. **Search**: Category filtering supports partial matching (case-insensitive).

## Error Response Format

All errors follow this format:
```json
{
  "detail": "Error message here"
}
```

## Testing

To test the API manually, use the Swagger UI at `http://localhost:8000/docs` after starting the server.

### Quick Test Flow

1. Create a user (as admin)
2. Create some records (as analyst)
3. View dashboard summary
4. Try unauthorized access (should fail)

## Future Enhancements

- JWT token-based authentication
- Rate limiting middleware
- Database migrations with Alembic
- Comprehensive unit and integration tests
- API versioning
- Soft delete for records
- Recurring transactions
- Budget management
- CSV export functionality
- Advanced filtering and search
- WebSocket real-time updates

## Project Structure Philosophy

This implementation follows clean architecture principles:

- **Models**: Database schema definition
- **Schemas**: Request/response validation
- **Services**: Core business logic (isolated from HTTP)
- **Routes**: HTTP endpoints (thin layer)
- **Core**: Configuration and security policies
- **Utils**: Shared dependencies and utilities

This separation ensures the business logic is testable and independent of the web framework.

## Notes

- The application creates an SQLite database file in the project root
- All timestamps are in UTC format
- The mock authentication uses simple headers for development
- The dashboard summary returns recent records (last 5) in reverse chronological order
- Category totals show net amounts (income positive, expense negative)

---

**Assignment Objective**: This backend demonstrates clean architecture, access control, data modeling, and practical API design for a finance management system.

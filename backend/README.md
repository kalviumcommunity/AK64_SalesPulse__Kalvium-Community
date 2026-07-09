# 🚀 SalesPulse AI Backend Foundation

> **Enterprise-Grade Node.js, Express, & Prisma (PostgreSQL) Backend Architecture**

SalesPulse AI is an AI-powered B2B Sales Behaviour Intelligence Platform. This repository hosts the backend API, structured using **Clean Architecture** patterns, modular service-oriented boundaries, and a scalable database repository layer.

---

## 🏗️ Folder Structure

The application is structured to ensure segregation of concerns, easy testability, and fast iteration:

```text
backend/
│
├── prisma/
│   └── schema.prisma         # Prisma Schema definitions & relationships
│
├── src/
│   ├── config/
│   │   └── env.js            # Environment variable validation & exports
│   │
│   ├── controllers/          # Request handlers & response coordination
│   │   ├── activityController.js
│   │   ├── analyticsController.js
│   │   ├── customerController.js
│   │   ├── dealController.js
│   │   ├── emailController.js
│   │   ├── recommendationController.js
│   │   └── userController.js
│   │
│   ├── database/
│   │   └── prisma.js         # Singleton Prisma client instance
│   │
│   ├── middlewares/          # Express middlewares
│   │   ├── errorHandler.js   # Global operational & query error interceptor
│   │   ├── notFoundHandler.js# 404 Route handler
│   │   ├── requestLogger.js  # Morgan configuration
│   │   └── validationHandler.js # Validation result parsing
│   │
│   ├── repositories/         # Database-abstracted query logic (BaseRepository)
│   │   ├── baseRepository.js
│   │   ├── activityRepository.js
│   │   ├── customerRepository.js
│   │   ├── dealRepository.js
│   │   ├── emailRepository.js
│   │   ├── recommendationRepository.js
│   │   └── userRepository.js
│   │
│   ├── routes/               # Express routing layer
│   │   ├── index.js          # Main router registry (aggregates /api/v1)
│   │   ├── activityRoutes.js
│   │   ├── analyticsRoutes.js
│   │   ├── customerRoutes.js
│   │   ├── dealRoutes.js
│   │   ├── emailRoutes.js
│   │   ├── recommendationRoutes.js
│   │   └── userRoutes.js
│   │
│   ├── services/             # Core business orchestrations
│   │   ├── activityService.js
│   │   ├── analyticsService.js
│   │   ├── customerService.js
│   │   ├── dealService.js
│   │   ├── emailService.js
│   │   ├── recommendationService.js
│   │   └── userService.js
│   │
│   ├── validators/           # express-validator schemas
│   │   ├── activityValidator.js
│   │   ├── customerValidator.js
│   │   ├── dealValidator.js
│   │   ├── emailValidator.js
│   │   ├── recommendationValidator.js
│   │   └── userValidator.js
│   │
│   ├── constants/            # Common enums & HTTP status codes
│   │   └── index.js
│   │
│   ├── utils/                # General-purpose utility helpers
│   │   ├── apiResponse.js
│   │   ├── appError.js
│   │   └── catchAsync.js
│   │
│   ├── app.js                # Express app middleware mapping
│   └── server.js             # Process exception wrappers & server listener
│
├── .env                      # Application environment configurations
├── package.json
└── README.md                 # Project README
```

---

## 🛠️ Tech Stack & Integration

- **Node.js** & **Express.js** (configured with ES Modules `"type": "module"`)
- **NeonDB** (PostgreSQL) as primary SQL database
- **Prisma ORM** for type-safe schema mapping and querying
- **express-validator** for schema request parsing
- **cookie-parser**, **cors**, **helmet** for standard security and parsing
- **morgan** for developer/production logging

---

## 🗄️ Database Design (Prisma Schemas)

The PostgreSQL schema is managed via Prisma in `prisma/schema.prisma` and maps the following core models:

### Models & Enums

- **User**: Sales reps, managers, and admins.
- **Customer**: Target B2B accounts.
- **Deal**: Value, pipeline stage, and relations.
- **Activity**: Logs of calls, meetings, notes, tasks, or emails.
- **Email**: Detailed email body logs, sentiment analyses, and confidence scores.
- **Recommendation**: Personalized AI-driven coaching suggestions.

### Relations Map
```mermaid
erDiagram
    users ||--o{ deals : "manages"
    users ||--o{ activities : "logs"
    users ||--o{ emails : "sends/receives"
    users ||--o{ recommendations : "receives"
    
    customers ||--o{ deals : "owns"
    customers ||--o{ activities : "attends"
    customers ||--o{ emails : "participates"
    
    deals ||--o{ activities : "linked_to"
    deals ||--o{ emails : "linked_to"
    deals ||--o{ recommendations : "coaches_for"
```

---

## 🔌 API Versioning & Endpoints

All APIs are modular and prefixed with `/api/v1/`:

| Module | Base Path | Methods | Description |
| :--- | :--- | :--- | :--- |
| **System** | `GET /` | `GET` | Health Check |
| **Users** | `/api/v1/users` | `POST` / `GET` | Registration, login, profiles |
| **Customers** | `/api/v1/customers` | `POST` / `GET` | Customers CRUD entrypoints |
| **Deals** | `/api/v1/deals` | `POST` / `GET` | Sales pipeline entrypoints |
| **Activities** | `/api/v1/activities` | `POST` / `GET` | Sales activity logging |
| **Emails** | `/api/v1/emails` | `POST` / `GET` | Email communication inputs |
| **Analytics** | `/api/v1/analytics` | `GET` | Dashboard summaries & metrics |
| **Recommendations** | `/api/v1/recommendations` | `POST` / `GET` | AI Coaching suggestion boards |

---

## 🏁 How to Run

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment variables
Copy the template below to `.env` in the `backend/` directory:
```env
PORT=5000
DATABASE_URL="postgresql://neondb_owner:npg_TaEzw0IjSYn6@ep-rapid-dawn-atkiuxb9-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require&schema=salespulse"
JWT_SECRET="your_jwt_secret_key"
NODE_ENV=development
```

### 3. Generate Prisma Client
```bash
npm run prisma:generate
```

### 4. Push Database Schemas to NeonDB
```bash
npm run prisma:db-push
```

### 5. Start Development Server
```bash
npm run dev
```
The server will start at [http://localhost:5000](http://localhost:5000) with hot-reloading enabled.

---

## 🚀 Architectural Design Choices

1. **ES Modules (`import/export`)**: Modern standard JS instead of legacy CommonJS `require`.
2. **BaseRepository Abstraction**: Extensible patterns to centralize database queries, leaving services and controllers decoupled from the Prisma client.
3. **catchAsync Controller Wrapper**: Simplifies controllers by eliminating redundant `try/catch` boilerplate, delegating errors automatically to the global error middleware handler.
4. **Environment Isolation**: Utilizes NeonDB custom schema names (`schema=salespulse`) to keep other workspace database instances completely separate and pristine.

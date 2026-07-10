# 🚀 SalesPulse AI

> **AI-Powered Sales Behaviour Intelligence Platform for B2B Organizations**

SalesPulse AI is a full-stack web application that transforms traditional CRM data into actionable business intelligence. It analyzes sales activities, deal progression, and email communication to identify behavioural patterns that contribute to successful deal closures. Using Data Science and Machine Learning, the platform provides predictive insights and AI-powered coaching recommendations to improve sales performance.

---

# 📌 Problem Statement

A B2B sales organization maintains CRM updates, email response history, and deal-stage transitions, but sales coaching remains intuition-driven because no behavioural analysis identifies patterns linked to faster deal closures.

---

# 🎯 Objectives

* Analyze CRM data and sales activities.
* Perform sentiment analysis on sales emails.
* Identify behavioural patterns of successful sales representatives.
* Predict the probability of deal closure.
* Generate AI-powered coaching recommendations.
* Visualize key sales metrics through interactive dashboards.

---

# ✨ Key Features

## 🔐 Authentication

* User Registration & Login
* JWT-based Authentication
* Role-Based Access Control

## 📊 CRM Management

* Customer Management
* Deal Management
* Deal Stage Tracking
* Sales Activity Logging

## 📧 Email Analysis

* Email Upload
* Sentiment Analysis
* Communication Tone Detection

## 📈 Behaviour Analytics

* Response Time Analysis
* Follow-up Frequency Analysis
* Deal Closing Time Analysis
* Salesperson Performance Metrics

## 🤖 AI & Machine Learning

* Email Sentiment Analysis
* Behaviour Pattern Analysis
* Deal Success Prediction
* AI Recommendation Engine

## 📉 Dashboard

* Sales Pipeline
* Win/Loss Analysis
* Team Performance
* Behaviour Insights
* AI Recommendations

---

# 🏗️ System Architecture

```text
End User
    │
    ▼
React Frontend
    │
REST API (JWT)
    │
    ▼
Node.js + Express Backend
    ├────────► PostgreSQL Database
    └────────► FastAPI AI Service
                    │
                    ▼
      Analytics & Recommendation Engine
                    │
                    ▼
          Interactive Dashboard
```

---

# 🛠️ Tech Stack

## Frontend

* React.js
* Tailwind CSS
* React Router
* Axios
* Recharts

## Backend

* Node.js
* Express.js
* JWT Authentication

## Database

* PostgreSQL

## AI/ML

* Python
* FastAPI
* Scikit-learn
* Hugging Face Transformers
* Pandas

## Deployment

* Frontend: Vercel
* Backend: Render
* AI Service: Render
* Database: PostgreSQL

---

# 📂 Project Structure

```text
SalesPulse-AI/
│
├── frontend/          # React Application
├── backend/           # Node.js + Express APIs
├── ai-service/        # FastAPI + ML Models
├── database/          # SQL Scripts & Schema
├── docs/              # Documentation
├── assets/            # Images & Static Files
├── README.md
└── .gitignore
```

---

# 📊 Core Modules

* Authentication Module
* CRM Management Module
* Deal Management Module
* Activity Tracking Module
* Email Analysis Module
* Behaviour Analytics Module
* Predictive Analytics Module
* AI Recommendation Engine
* Dashboard & Reporting Module

---

# 🔄 Workflow

1. User logs into the system.
2. Sales data and customer information are managed through the CRM.
3. Email conversations are uploaded or synchronized.
4. The AI service analyzes email sentiment and communication tone.
5. Behavioural metrics such as response time, follow-up frequency, and deal progression are calculated.
6. Machine Learning models predict deal success probability.
7. The recommendation engine generates personalized coaching suggestions.
8. Interactive dashboards present insights for sales managers and representatives.

---

# 📈 Expected Outcomes

* Data-driven sales coaching
* Improved sales conversion rates
* Faster deal closure
* Behaviour-based performance evaluation
* AI-powered business insights
* Better decision-making for sales managers

---

# 👨‍💻 Team Responsibilities

### Frontend Developer

* User Interface
* Dashboard
* Charts & Visualizations
* Authentication Pages

### Backend Developer

* REST APIs
* Database Management
* CRM Services
* Authentication & Authorization

### AI/ML Developer

* Sentiment Analysis
* Behaviour Analytics
* Prediction Models
* Recommendation Engine

---

# 🚀 Future Enhancements

* Salesforce Integration
* HubSpot Integration
* Voice Call Sentiment Analysis
* WhatsApp Conversation Analysis
* Mobile Application
* Real-Time AI Sales Assistant
* Advanced Sales Forecasting
* LLM-Based Sales Coaching

---




# 📜 License

This project is developed for educational and research purposes as part of a Data Science and Machine Learning project.




















































































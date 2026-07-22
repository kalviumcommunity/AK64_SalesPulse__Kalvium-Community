# SalesPulse AI — AI-Powered Sales Behaviour Intelligence Platform for B2B Organizations
## Product Requirements Document (PRD)

**Problem statement** — A B2B sales organization maintains CRM updates, email response history, and deal-stage transitions independently, but sales coaching remains intuition-driven because no behavioural analysis identifies the patterns linked to faster, more successful deal closures.

| Field | Detail |
| --- | --- |
| **Version** | 1.0.0 |
| **Status** | Draft – In Development |
| **Created** | 2026-07-10 |
| **Last Updated** | 2026-07-10 |
| **Document Type** | Product Requirements Document |
| **Project** | SalesPulse AI |
| **Tech Stack** | Streamlit, Python, FastAPI, Node.js, Express.js, PostgreSQL, Scikit-learn, Hugging Face Transformers, Pandas, JWT, Plotly, Streamlit Community Cloud, Render |

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Business Problem](#2-business-problem)
3. [User Personas](#3-user-personas)
4. [User Pain Points](#4-user-pain-points)
5. [Project Goals](#5-project-goals)
6. [Dataset & Data Source Documentation](#6-dataset--data-source-documentation)
7. [Success Metrics](#7-success-metrics)
8. [Functional Requirements](#8-functional-requirements)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [User Stories](#10-user-stories)
11. [MVP Scope](#11-mvp-scope)
12. [Future Scope](#12-future-scope)
13. [Risks and Assumptions](#13-risks-and-assumptions)
14. [Acceptance Criteria](#14-acceptance-criteria)
- [Appendix A — Glossary](#appendix-a--glossary)
- [Appendix B — Data Schema Contracts](#appendix-b--data-schema-contracts)

---

## 1. Executive Summary
SalesPulse AI is a sales behaviour intelligence platform that transforms disconnected CRM records, activity logs, and email communication into actionable coaching insights. It helps sales representatives, sales managers, and revenue leaders move from intuition-driven coaching to data-driven performance management.

The platform answers the three most critical sales-enablement questions at any B2B organization:
What separates a top performer from an average one? Which deals are at risk of stalling? What should each rep do differently to close faster?

Built as a full-stack intelligence product using **Streamlit**, Python, Node.js, PostgreSQL, and machine learning, SalesPulse AI delivers:
- Real-time visibility into CRM activity, deal-stage progression, and communication quality
- Automated behavioural analysis linking response time, follow-up cadence, and tone to deal outcomes
- ML-powered deal success prediction and closing probability scoring
- AI-generated, personalized coaching recommendations for every sales representative

This document defines the full product requirements, user stories, MVP boundaries, and acceptance criteria needed to build, validate, and ship SalesPulse AI.

---

## 2. Business Problem

### 2.1 Context
Modern CRM platforms (Salesforce, HubSpot, Zoho, and custom in-house systems) generate large volumes of deal, activity, and communication data. While this data exists, it is typically:
- **Fragmented** — spread across CRM records, inboxes, and spreadsheets
- **Descriptive, not behavioural** — CRM shows what happened (stage changes, activity counts) but not why some reps close faster
- **Unanalyzed** — raw activity logs and email threads are rarely mined for behavioural patterns
- **Reactive** — coaching happens after a deal is lost, not while it can still be saved

### 2.2 The Core Gap
There is no unified intelligence layer that connects:

| Data Source | What it tells us |
| --- | --- |
| **CRM Deal Data** | What stage a deal is in and how it is progressing |
| **Activity Logs** | What actions a rep took and when |
| **Email Communication** | How a rep is engaging with a prospect |
| **Response Time & Follow-up Data** | How responsive and consistent a rep is |
| **Historical Win/Loss Data** | What behaviours actually correlate with closed-won deals |

Without connecting these dots, sales managers cannot answer why some reps consistently outperform others — only that they do.

### 2.3 Business Impact
- Sales managers coach based on gut feeling rather than evidence
- High-performing behaviours (fast response time, consistent follow-up, positive communication tone) are never systematically identified or replicated
- Deals stall or are lost without early warning signs being flagged
- New reps take longer to ramp because there is no data-backed playbook of what works

### 2.4 Opportunity
Organizations that implement behavioural sales analytics and AI coaching consistently report meaningful improvements in conversion rate and sales cycle length. SalesPulse AI aims to make that level of intelligence accessible to small and mid-sized B2B sales teams without requiring enterprise-grade CRM add-ons.

---

## 3. User Personas

### 3.1 Persona 1 — The Sales Representative
**Name:** Aditya Kulkarni | **Role:** Account Executive  
**Background:** Manages a pipeline of 20–30 active deals across multiple accounts. Spends most of the day on calls, emails, and CRM updates.

| Attribute | Detail |
| --- | --- |
| **Primary Goal** | Understand what he could be doing better to close deals faster |
| **Frustration** | Feedback from managers is vague and comes too late to act on |
| **Tool Comfort** | Medium — comfortable with CRM UI and Streamlit dashboards, not with raw data |
| **Success** | Gets clear, specific coaching tips tied to his own deals |

### 3.2 Persona 2 — The Sales Manager
**Name:** Meera Nair | **Role:** Sales Team Manager  
**Background:** Leads a team of 8 account executives. Responsible for team quota and coaching.

| Attribute | Detail |
| --- | --- |
| **Primary Goal** | Identify which reps and behaviours are driving (or blocking) deal closures |
| **Frustration** | 1:1 coaching sessions rely on anecdotes, not evidence |
| **Tool Comfort** | High — comfortable with dashboards and CRM reporting |
| **Success** | Can pinpoint a rep's weak behavioural pattern within minutes |

### 3.3 Persona 3 — The VP of Sales
**Name:** Rohan Bhatt | **Role:** VP of Sales  
**Background:** Accountable for overall revenue targets across all sales teams. Reviews pipeline health monthly.

| Attribute | Detail |
| --- | --- |
| **Primary Goal** | High-level view of team performance, win/loss trends, and pipeline risk |
| **Frustration** | Standard CRM reports show pipeline value but not the behavioural drivers behind it |
| **Tool Comfort** | Low on raw data — needs clean, narrative dashboards |
| **Success** | Gets a clear performance and risk summary before every leadership review |

### 3.4 Persona 4 — The RevOps / Sales Ops Analyst
**Name:** Ishita Ghosh | **Role:** Revenue Operations Analyst  
**Background:** Owns CRM data quality and sales process tooling. Supports the sales team with reporting and system configuration.

| Attribute | Detail |
| --- | --- |
| **Primary Goal** | Ensure CRM and email data is clean, structured, and reliably feeding analytics |
| **Frustration** | Inconsistent activity logging and missing email metadata break reports |
| **Tool Comfort** | Very High — SQL, APIs, backend systems |
| **Success** | Pipelines run reliably with clear error logs and no manual cleanup |

---

## 4. User Pain Points

| # | Persona | Pain Point | Severity |
| --- | --- | --- | --- |
| **P1** | Sales Manager | Cannot identify which specific behaviours separate top performers from the rest | 🔴 Critical |
| **P2** | Sales Representative | Receives generic feedback with no tie-back to his own deal activity | 🔴 Critical |
| **P3** | VP of Sales | Monthly reports show pipeline value but no behavioural or predictive signals | 🟠 High |
| **P4** | Sales Manager | Deals at risk of stalling are discovered only after they are lost | 🔴 Critical |
| **P5** | Sales Representative | No visibility into how his response time or follow-up cadence compares to top performers | 🟠 High |
| **P6** | VP of Sales | Cannot predict which deals are likely to close this quarter | 🟠 High |
| **P7** | RevOps Analyst | Activity and email data is inconsistently logged, making analysis unreliable | 🟡 Medium |
| **P8** | All Personas | No single system connects CRM activity, email communication, and deal outcomes | 🔴 Critical |
| **P9** | Sales Manager | Coaching recommendations from existing tools are generic, not tied to actual behaviour patterns | 🟡 Medium |
| **P10** | Sales Representative | Cannot tell whether a stalled deal is due to communication tone, slow response, or lack of follow-up | 🟠 High |

---

## 5. Project Goals

### 5.1 Primary Goals
| Goal | Description |
| --- | --- |
| **G1 — Behavioural Visibility** | Provide a unified view of sales activity, response time, and follow-up frequency across reps and teams |
| **G2 — Communication Quality Analysis** | Evaluate email sentiment and tone to assess communication effectiveness |
| **G3 — Pattern Identification** | Identify behavioural patterns that correlate with successful deal closures |
| **G4 — Predictive Insights** | Predict deal success probability using machine learning |
| **G5 — Performance Metrics** | Calculate key sales performance metrics per rep and per team |
| **G6 — AI Coaching** | Surface specific, data-backed coaching recommendations for each representative |

### 5.2 Secondary Goals
| Goal | Description |
| --- | --- |
| **G7 — Manager & Executive Reporting** | Generate role-specific dashboards for reps, managers, and leadership |
| **G8 — Data Product Foundation** | Build a reusable, modular architecture (CRM, AI service, Streamlit app) for future extension |
| **G9 — Coaching Culture** | Enable a culture of evidence-based, continuous sales coaching |

---

## 6. Dataset & Data Source Documentation

| Data Source | Owner | Key Fields | Data Quality / Validation | Refresh Rate |
| --- | --- | --- | --- | --- |
| **CRM Deal Data** | Sales Team / CRM System | `deal_id`, `customer_id`, `salesperson_id`, `deal_value`, `current_stage`, `status`, `created_date`, `closed_date` | Schema validated before ingestion; stage transitions checked for consistency | Real-time / on update |
| **Customer Data** | Sales Team | `customer_id`, `company_name`, `contact_person`, `email`, `phone_number` | Duplicate customer records deduplicated | On update |
| **Activity Data** | Sales Representatives (CRM logging) | `activity_id`, `deal_id`, `activity_type`, `activity_date`, `notes` | Missing activity types flagged; timestamps validated | Real-time / on update |
| **Email Communication Data** | Email Upload / Integration | `email_id`, `deal_id`, `sender`, `receiver`, `subject`, `email_body`, `sentiment_score`, `sent_timestamp` | PII handling reviewed; malformed emails logged and skipped | On upload |
| **User / Role Data** | Admin | `user_id`, `name`, `email`, `role` | Role mappings verified before processing | On update |

### Data Validation Requirements
- All datasets must pass schema validation before ingestion.
- Missing or malformed records must be identified and logged without interrupting the pipeline.
- Duplicate records must be detected and removed during preprocessing.
- All processed datasets must conform to the defined schema before analytics and machine learning workflows are executed.

---

## 7. Success Metrics

### 7.1 Product Metrics (KPIs)
| Metric | Target | Measurement Method |
| --- | --- | --- |
| **Time-to-Insight** | < 5 minutes from data upload to behavioural insight | User testing & session recording |
| **Coaching Recommendation Relevance** | ≥ 85% rated "relevant" by sales managers in review | Manager feedback survey |
| **Deal Success Prediction Accuracy** | ≥ 80% accuracy on labeled historical deals | ML model evaluation |
| **Sentiment/Tone Classification Accuracy** | ≥ 85% accuracy against labeled email test set | NLP model evaluation |
| **Dashboard Load Time** | < 3 seconds on standard hardware | Performance testing |
| **Data Freshness** | Near real-time activity sync with < 1% data loss | Pipeline monitoring |

### 7.2 Business Metrics
| Metric | Target |
| --- | --- |
| **Reduction in average sales cycle length** | ≥ 15% reduction vs. baseline |
| **Increase in deal conversion rate** | ≥ 10% improvement |
| **% of deals with a behavioural risk flag caught before stalling** | ≥ 70% |

### 7.3 Technical Metrics
| Metric | Target |
| --- | --- |
| **Backend/API test coverage** | ≥ 80% |
| **Data schema validation pass rate** | 100% on processed datasets |
| **API uptime during evaluation period** | ≥ 99% |

---

## 8. Functional Requirements

### 8.1 Authentication Module
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-01** | The system SHALL allow new user registration | Must Have |
| **FR-02** | The system SHALL support secure login using JWT authentication | Must Have |
| **FR-03** | The system SHALL support role-based access control (Rep / Manager / Admin) | Must Have |
| **FR-04** | The system SHALL manage user sessions securely | Must Have |

### 8.2 CRM Management Module
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-05** | The system SHALL allow creation, update, and deletion of customer records | Must Have |
| **FR-06** | The system SHALL allow creation and tracking of deals through defined stages | Must Have |
| **FR-07** | The system SHALL log deal stage transitions with timestamps | Must Have |
| **FR-08** | The system SHALL track sales activities linked to each deal | Must Have |
| **FR-09** | The system SHALL allow viewing of full deal history | Must Have |

### 8.3 Email Analysis Module
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-10** | The system SHALL allow upload and storage of email conversations linked to a deal | Must Have |
| **FR-11** | The system SHALL analyze email sentiment using NLP | Must Have |
| **FR-12** | The system SHALL detect communication tone (e.g., assertive, passive, positive, negative) | Must Have |
| **FR-13** | The system SHALL store computed sentiment scores against each email record | Must Have |

### 8.4 Behaviour Analytics Module
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-14** | The system SHALL compute average response time per representative | Must Have |
| **FR-15** | The system SHALL compute follow-up frequency per deal and per representative | Must Have |
| **FR-16** | The system SHALL compute average deal closing time | Must Have |
| **FR-17** | The system SHALL compute a salesperson performance score based on behavioural metrics | Should Have |
| **FR-18** | The system SHALL summarize sales activity volume and type per representative | Must Have |

### 8.5 Predictive Analytics Module
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-19** | The system SHALL train a model to predict deal success probability | Must Have |
| **FR-20** | The system SHALL output a closing probability score per active deal | Must Have |
| **FR-21** | The system SHALL predict expected sales performance trends per representative | Should Have |
| **FR-22** | The system SHALL retrain models when new labeled deal outcome data is available | Should Have |

### 8.6 AI Recommendation Engine
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-23** | The system SHALL generate personalized coaching recommendations per representative | Must Have |
| **FR-24** | The system SHALL suggest behaviour improvements based on identified weak metrics | Must Have |
| **FR-25** | The system SHALL recommend optimal follow-up timing per deal | Should Have |
| **FR-26** | The system SHALL suggest communication tone/style improvements based on NLP analysis | Should Have |

### 8.7 Dashboard Module (Streamlit)
| ID | Requirement | Priority |
| --- | --- | --- |
| **FR-27** | The dashboard SHALL render a Sales Performance view with individual and team metrics | Must Have |
| **FR-28** | The dashboard SHALL render a Pipeline Analytics view with stage-wise deal distribution | Must Have |
| **FR-29** | The dashboard SHALL render a Win/Loss Analysis view | Must Have |
| **FR-30** | The dashboard SHALL render a Behaviour Analytics view (response time, follow-up frequency, tone) | Must Have |
| **FR-31** | The dashboard SHALL render a Team Performance view for managers | Must Have |
| **FR-32** | The dashboard SHALL support filtering by representative, team, and date range | Must Have |

---

## 9. Non-Functional Requirements

### 9.1 Performance
| ID | Requirement |
| --- | --- |
| **NFR-01** | Dashboard must load within 3 seconds on a standard laptop with sample datasets |
| **NFR-02** | Behavioural analytics computation must complete within 5 minutes for a full quarter of activity data |
| **NFR-03** | AI prediction and recommendation services must return results within 2 seconds |

### 9.2 Reliability
| ID | Requirement |
| --- | --- |
| **NFR-04** | Email/CRM ingestion must handle malformed records gracefully without crashing |
| **NFR-05** | All pipeline and service failures must be logged with a descriptive error message |
| **NFR-06** | The system must maintain 99% uptime during demo and evaluation periods |

### 9.3 Maintainability
| ID | Requirement |
| --- | --- |
| **NFR-07** | All code must follow consistent linting and style standards |
| **NFR-08** | All functions and modules must have docstrings/comments |
| **NFR-09** | Unit tests must achieve ≥ 80% code coverage |
| **NFR-10** | CI must run automatically on every push to main or develop |

### 9.4 Portability
| ID | Requirement |
| --- | --- |
| **NFR-11** | The Streamlit frontend and AI service must run on Python 3.10+ and the backend on Node.js 18+ |
| **NFR-12** | All environment configuration must be managed via `.env` files |

### 9.5 Security
| ID | Requirement |
| --- | --- |
| **NFR-13** | Passwords must be securely hashed; no plaintext credentials stored |
| **NFR-14** | JWT tokens must expire and be securely validated on every request |
| **NFR-15** | No real customer PII should be committed to the repository |

### 9.6 Usability
| ID | Requirement |
| --- | --- |
| **NFR-16** | The Streamlit dashboard must be navigable by a non-technical sales manager without training |
| **NFR-17** | All charts (Plotly / Streamlit charts) must include axis labels, titles, and tooltips |

---

## 10. User Stories

### Epic 1 — Authentication
**US-101** — As a user, I want to register and log in securely, so that I can access my personalized sales data.  
*Acceptance Criteria:*
- Registration requires name, email, and password
- Login issues a valid JWT token
- Role (Rep / Manager / Admin) determines dashboard access in Streamlit

### Epic 2 — CRM Management
**US-201** — As a Sales Representative, I want to manage my deals and customers in one place, so that I don't need a separate CRM tool.  
*Acceptance Criteria:*
- Reps can create, update, and view deals and customers
- Deal stage changes are logged with timestamps
- Activity history is visible per deal

### Epic 3 — Email Analysis
**US-301** — As a Sales Representative, I want my email threads analyzed for sentiment and tone, so that I understand how my communication is being received.  
*Acceptance Criteria:*
- Uploaded emails are processed and a sentiment score is generated
- Tone classification is displayed per email and aggregated per deal
- Sentiment trend is visible over the life of a deal

### Epic 4 — Behaviour Analytics
**US-401** — As a Sales Manager, I want to see response time and follow-up frequency for each rep, so that I can identify behavioural gaps.  
*Acceptance Criteria:*
- Response time and follow-up frequency are computed per rep and per deal
- Metrics are benchmarked against top-performer averages
- Underperforming metrics are visually flagged

### Epic 5 — Predictive Analytics
**US-501** — As a Sales Manager, I want to see a closing probability score for each open deal, so that I can prioritize coaching and support where it matters most.  
*Acceptance Criteria:*
- Every open deal displays a closing probability score
- Score updates as new activity/email data is added
- Model accuracy is tracked and reported

### Epic 6 — AI Recommendation Engine
**US-601** — As a Sales Representative, I want personalized coaching tips based on my own deal activity, so that I know exactly what to improve.  
*Acceptance Criteria:*
- Recommendations are generated per rep, tied to specific weak metrics
- Each recommendation includes the issue, the metric it's based on, and a suggested action
- At least 3 recommendations are surfaced per rep per review cycle

### Epic 7 — Dashboard
**US-701** — As a VP of Sales, I want a high-level performance and pipeline view, so that I can assess team health before leadership reviews.  
*Acceptance Criteria:*
- Executive-level view in Streamlit shows team performance, win/loss trends, and pipeline distribution
- Sidebar filters support team, rep, and date range
- View loads in under 3 seconds

---

## 11. MVP Scope
The MVP focuses on validating the core value proposition: connect CRM activity and email communication to surface behavioural insights and AI coaching automatically.

### ✅ Included in MVP
| Feature | Rationale |
| --- | --- |
| **User authentication (JWT, role-based access)** | Foundation for all role-specific views |
| **CRM management (customers, deals, activities)** | Foundation for everything else |
| **Email upload with sentiment and tone analysis** | Core value — communication quality |
| **Response time and follow-up frequency analytics** | Core value — behavioural visibility |
| **Deal success prediction model** | Core value — predictive signal |
| **AI-generated coaching recommendations** | Core value — actionable output |
| **Sales Performance, Pipeline, and Behaviour dashboards (Streamlit)** | Primary delivery surface |
| **Sample/simulated CRM and email datasets** | Enables demo without real customer data |

### ❌ Explicitly Excluded from MVP
| Feature | Reason for Deferral |
| --- | --- |
| **Integration with Salesforce / HubSpot** | Adds integration complexity; MVP uses internal CRM module |
| **Voice call sentiment analysis** | Requires speech-to-text pipeline; Phase 2 |
| **WhatsApp / chat conversation analysis** | External integration; Phase 2 |
| **Real-time AI sales assistant** | Requires conversational AI infrastructure; Phase 2 |
| **Mobile application** | Streamlit web dashboard is sufficient for MVP validation |
| **Deep-learning-based forecasting** | Classical ML sufficient for MVP accuracy targets |

---

## 12. Future Scope

### Phase 2 — Intelligence Layer
| Feature | Description |
| --- | --- |
| **Voice Call Sentiment Analysis** | Analyze recorded sales calls for tone and engagement signals |
| **WhatsApp & Chat Analysis** | Extend communication analysis beyond email |
| **Real-Time AI Sales Assistant** | Conversational assistant offering in-the-moment coaching |
| **LLM-Powered Conversational Insights** | Natural language Q&A over sales and behavioural data |

### Phase 3 — Scale & Integration
| Feature | Description |
| --- | --- |
| **Salesforce / HubSpot Integration** | Ingest and sync deal and activity data from external CRMs |
| **Advanced Forecasting** | Deep-learning-based sales performance forecasting |
| **Mobile Application** | On-the-go access to coaching insights and deal alerts |
| **Role-Based Data Scoping** | Reps see only their own data; managers see their team's data |

### Phase 4 — Enterprise Readiness
| Feature | Description |
| --- | --- |
| **SaaS Deployment** | Containerized deployment on cloud infrastructure |
| **Public API Layer** | REST API for programmatic access to behavioural intelligence |
| **Audit Trail** | Log all AI recommendations and predictions for compliance |
| **Custom Coaching Rules** | Allow managers to define their own behavioural thresholds |

---

## 13. Risks and Assumptions

### 13.1 Risks
| # | Risk | Probability | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| **R1** | Simulated CRM/email data may not reflect real-world sales complexity | Medium | High | Design schemas based on real CRM export formats |
| **R2** | ML models may underperform on small or synthetic datasets | High | Medium | Use cross-validation; document accuracy clearly; set realistic targets |
| **R3** | Sentiment/tone analysis may misclassify domain-specific sales language | Medium | Medium | Fine-tune or validate NLP model against sales-specific email samples |
| **R4** | Dashboard performance may degrade with large activity datasets | Medium | Medium | Implement caching (`st.cache_data`) and pagination |
| **R5** | Schema inconsistencies across CRM and email datasets | Medium | High | Define and enforce a strict schema contract |
| **R6** | Scope creep beyond MVP boundaries | High | High | Strict adherence to MVP scope; defer all Phase 2+ features |
| **R7** | Behaviour-to-outcome correlation may be weak in synthetic data | Medium | High | Explicitly engineer realistic correlations in data generation scripts |

### 13.2 Assumptions
| # | Assumption |
| --- | --- |
| **A1** | Sample/simulated CRM and email data is used for MVP; no live CRM API connection required |
| **A2** | Simulated datasets can adequately represent real-world sales behaviour patterns for MVP validation |
| **A3** | Streamlit + Python / Node.js + PostgreSQL is the accepted primary application stack |
| **A4** | Node.js 18+ and Python 3.10+ are available in the development environment |
| **A5** | GitHub is the version control and CI/CD platform |
| **A6** | All team members are familiar with Python, Streamlit, Node.js, and ML |
| **A7** | The project will be evaluated in a demo environment, not a production sales organization |

---

## 14. Acceptance Criteria
The following criteria define the minimum bar for the SalesPulse AI MVP to be considered complete and ready for evaluation.

- **AC-1 — Authentication & Access**
  - Users can register and log in securely with JWT-based sessions
  - Role-based access correctly restricts Streamlit dashboard views (Rep / Manager / Admin)
- **AC-2 — CRM Management**
  - Deals, customers, and activities can be created, updated, and viewed without errors
  - Deal stage transitions are logged with accurate timestamps
- **AC-3 — Email & Behaviour Analytics**
  - Uploaded emails are processed and assigned a sentiment score and tone label
  - Response time and follow-up frequency are computed correctly for all reps in the dataset
  - Metrics are accurate to within an acceptable tolerance verified against source activity logs
- **AC-4 — Machine Learning**
  - Deal success prediction model achieves the target accuracy on the held-out test set
  - Model training and inference scripts run end-to-end without errors
  - Model artifacts are saved and reloadable without retraining
- **AC-5 — AI Recommendation Engine**
  - At least 3 personalized coaching recommendations are generated per representative
  - Each recommendation is tied to a specific behavioural metric or communication signal
- **AC-6 — Dashboard (Streamlit)**
  - All Streamlit dashboard views (Sales Performance, Pipeline, Win/Loss, Behaviour, Team) render without errors
  - Filters (rep, team, date range) work correctly across all views
  - Dashboard loads in under 3 seconds on a standard laptop
- **AC-7 — Code Quality & Documentation**
  - Backend, Streamlit frontend, and AI service code passes linting with no errors
  - Unit test coverage ≥ 80%
  - CI pipeline runs successfully on the main branch
  - PRD is complete and version-controlled
  - README includes setup instructions, architecture overview, and screenshots

---

## Appendix A — Glossary
| Term | Definition |
| --- | --- |
| **Behavioural Analytics** | Analysis of sales activity patterns (response time, follow-up, tone) linked to deal outcomes |
| **Sentiment Analysis** | NLP technique used to determine the emotional tone of a piece of text |
| **Closing Probability Score** | An ML-generated score estimating the likelihood a deal will close successfully |
| **Follow-up Frequency** | The rate at which a sales rep re-engages a prospect after initial contact |
| **Salesperson Performance Score** | A composite score representing a rep's overall behavioural and outcome performance |
| **Coaching Recommendation** | An AI-generated, data-backed suggestion for improving a rep's sales behaviour |
| **JWT** | JSON Web Token — used for secure, stateless user authentication |

---

## Appendix B — Data Schema Contracts

### Users
```sql
user_id       : UUID / INT (PK)
name          : VARCHAR(100)
email         : VARCHAR(150)
password      : VARCHAR(255)  (hashed)
role          : VARCHAR(50)   (rep | manager | admin)
```

### Customers
```sql
customer_id     : UUID / INT (PK)
company_name    : VARCHAR(150)
contact_person  : VARCHAR(100)
email           : VARCHAR(150)
phone_number    : VARCHAR(20)
```

### Deals
```sql
deal_id         : UUID / INT (PK)
customer_id     : FK -> Customers
salesperson_id  : FK -> Users
deal_value      : DECIMAL(12,2)
current_stage   : VARCHAR(50)
status          : VARCHAR(20)   (open | won | lost)
created_date    : DATE
closed_date     : DATE (nullable)
```

### Activities
```sql
activity_id     : UUID / INT (PK)
deal_id         : FK -> Deals
activity_type   : VARCHAR(50)   (call | email | meeting | note)
activity_date   : DATETIME
notes           : TEXT
```

### Emails
```sql
email_id        : UUID / INT (PK)
deal_id         : FK -> Deals
sender          : VARCHAR(150)
receiver        : VARCHAR(150)
subject         : VARCHAR(200)
email_body      : TEXT
sentiment_score : DECIMAL(4,3)
sent_timestamp  : DATETIME
```

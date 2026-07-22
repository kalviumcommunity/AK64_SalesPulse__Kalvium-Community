# SalesPulse AI — Functional Specification
## What to Build, Feature by Feature, and How the Website Should Work

This document translates the PRD into a build-ready functional spec: every page, every function, every piece of logic, and how data moves through the system end to end.

---

## 1. How the Whole System Works (End-to-End Flow)

```
1. User opens the site → lands on Login (or Signup if new)
2. User logs in → JWT issued → redirected to role-based dashboard
3. Rep/Manager adds/updates CRM data (customers, deals, activities)
   OR uploads email threads tied to a deal
4. Backend stores raw data in PostgreSQL
5. AI Service (FastAPI) periodically/on-demand:
   a. Cleans & processes CRM + email data
   b. Runs NLP sentiment/tone analysis on emails
   c. Computes behavioural metrics (response time, follow-up frequency, etc.)
   d. Runs ML model → deal success probability + closing score
   e. Runs recommendation engine → coaching tips
   f. Writes results back to PostgreSQL (AI Results tables)
6. Node.js backend serves processed analytics + AI results via REST API
7. Streamlit frontend renders role-specific dashboards (Rep / Manager / VP / Admin)
8. User acts on insights (updates a deal, follows up faster, etc.) → cycle repeats
```

**Core principle:** CRM data and Email data are the *inputs*. Behavioural Analytics, Predictive Analytics, and the Recommendation Engine are *derived outputs*. The Dashboard is just a window into those outputs — it should never compute anything itself, only display what the backend/AI service already calculated.

---

## 2. System Roles & What Each Role Can Do

| Role | Can Do |
|---|---|
| **Sales Representative** | View/manage own deals & customers, upload own emails, view own behaviour metrics and coaching tips |
| **Sales Manager** | Everything a Rep can do + view all reps on their team, compare rep performance, view team-level dashboards |
| **VP / Admin** | Everything a Manager can do + view all teams, manage users/roles, view org-wide executive dashboard |

This role logic must be enforced **both** in the UI (hide/show nav items) and in the **backend API** (never trust the frontend alone — every endpoint checks the JWT role/claims).

---

## 3. Page-by-Page Functional Breakdown

### 3.1 Login Page
**Purpose:** Authenticate an existing user.

| Function | Behavior |
|---|---|
| `validateLoginForm()` | Checks email format + password not empty before submit |
| `loginUser(email, password)` | POST `/api/auth/login` → returns JWT + user role |
| `storeSession(token)` | Stores JWT (in memory/context, not localStorage in the artifact demo — real app uses httpOnly cookie or secure storage) |
| `redirectByRole(role)` | Rep → `/performance`, Manager → `/team`, VP/Admin → `/performance` (org view) |

### 3.2 Signup Page
**Purpose:** Register a new user.

| Function | Behavior |
|---|---|
| `validateSignupForm()` | Checks all fields filled, password match, email format |
| `registerUser(name, email, password, role)` | POST `/api/auth/register` → hashes password server-side, creates user |
| `autoLoginAfterSignup()` | On success, log the user in immediately and redirect |

### 3.3 Sales Performance Dashboard (Rep + Manager + VP view, scoped by role)
**Purpose:** Show performance metrics relevant to the logged-in user's scope.

| Function | Behavior |
|---|---|
| `getPerformanceSummary(userId/teamId, dateRange)` | GET `/api/analytics/performance` → deals closed, win rate, avg cycle time, avg response time |
| `getPipelineByStage(scope, dateRange)` | GET `/api/deals/pipeline-summary` → count/value per stage |
| `getEmailToneBreakdown(scope, dateRange)` | GET `/api/emails/tone-summary` → positive/neutral/negative counts |
| `getCoachingRecommendations(userId)` | GET `/api/ai/recommendations/:userId` → top 3+ AI tips |
| `applyFilters(dateRange, rep/team)` | Re-fetches all of the above with new query params |

### 3.4 Pipeline Analytics Page
**Purpose:** Deal-level visibility into open pipeline.

| Function | Behavior |
|---|---|
| `getPipelineValueByStage(scope, dateRange)` | GET `/api/deals/value-by-stage` |
| `getActiveDeals(scope, filters)` | GET `/api/deals?status=open` → deal list with stage, value, closing probability |
| `getClosingProbability(dealId)` | Pulled from AI Results table (pre-computed by ML service, not computed live) |
| `filterDealsByStageOrRep()` | Client-side or query-param filtering on the same dataset |

### 3.5 Win/Loss Analysis Page
**Purpose:** Understand historical outcomes.

| Function | Behavior |
|---|---|
| `getWinLossSummary(scope, dateRange)` | GET `/api/deals/win-loss-summary` → won, lost, win rate |
| `getWinRateTrend(scope, period)` | GET `/api/deals/win-rate-trend?groupBy=month` |
| `getLossReasons(scope, dateRange)` | GET `/api/deals/loss-reasons` (from `notes`/`activity_type` tagging or a `loss_reason` field on Deals) |
| `getWinRateByRep(teamId, dateRange)` | GET `/api/deals/win-rate-by-rep` → table data |

### 3.6 Behaviour Analytics Page
**Purpose:** Surface the core differentiator — behavioural metrics.

| Function | Behavior |
|---|---|
| `getResponseTimeMetrics(scope, dateRange)` | GET `/api/behaviour/response-time` |
| `getFollowUpFrequency(scope, dateRange)` | GET `/api/behaviour/follow-up-frequency` |
| `getFollowUpTrend(scope, period)` | GET `/api/behaviour/follow-up-trend?groupBy=week` |
| `getBehaviourScorecard(teamId)` | GET `/api/behaviour/scorecard` → response time, follow-ups, tone score, composite behaviour score per rep |
| `computeBehaviourScore(metrics)` *(AI service, not frontend)* | Weighted formula combining response time, follow-up frequency, and tone into a 0–100 score |

### 3.7 Team Performance Page (Manager/VP only)
**Purpose:** Manager-facing rollup + coaching queue.

| Function | Behavior |
|---|---|
| `getTeamQuotaAttainment(teamId, period)` | GET `/api/team/quota-attainment` |
| `getLeaderboard(teamId, period)` | GET `/api/team/leaderboard` → ranked reps by attainment |
| `getManagerNotesQueue(teamId)` | GET `/api/ai/manager-notes/:teamId` → AI-flagged reps needing attention |
| `restrictToManagerScope(userId)` | Backend middleware — a Manager only ever sees their own team's `team_id` |

### 3.8 CRM Management (Deals, Customers, Activities) — used inside Pipeline/Performance pages or a dedicated CRM screen
| Function | Behavior |
|---|---|
| `createCustomer(data)` | POST `/api/customers` |
| `updateCustomer(id, data)` | PUT `/api/customers/:id` |
| `createDeal(data)` | POST `/api/deals` |
| `updateDealStage(dealId, newStage)` | PATCH `/api/deals/:id/stage` → also logs a stage-transition Activity automatically |
| `deleteDeal(dealId)` | DELETE `/api/deals/:id` |
| `logActivity(dealId, type, notes)` | POST `/api/activities` |
| `getDealHistory(dealId)` | GET `/api/deals/:id/history` → all activities + stage changes chronologically |

### 3.9 Email Analysis (upload flow)
| Function | Behavior |
|---|---|
| `uploadEmail(dealId, emailData)` | POST `/api/emails` → stores raw email |
| `triggerSentimentAnalysis(emailId)` | Backend calls AI Service `/analyze/sentiment` → stores `sentiment_score` |
| `triggerToneDetection(emailId)` | Backend calls AI Service `/analyze/tone` → stores tone label |
| `getEmailsForDeal(dealId)` | GET `/api/emails?dealId=` → full thread with sentiment/tone shown inline |

---

## 4. AI Service Functions (Python / FastAPI)

| Function | Purpose |
|---|---|
| `analyze_sentiment(email_body)` | Returns a sentiment score (-1 to 1) using a Hugging Face transformer model |
| `detect_tone(email_body)` | Classifies tone: positive / neutral / negative / assertive / passive |
| `compute_response_time(activities)` | Calculates average time between inbound and outbound communication per deal |
| `compute_follow_up_frequency(activities)` | Counts follow-up activities per deal over time |
| `compute_behaviour_score(rep_metrics)` | Weighted composite score (0–100) from response time, follow-ups, tone |
| `predict_deal_success(deal_features)` | Scikit-learn classifier → probability (0–1) a deal closes won |
| `predict_closing_probability(deal_id)` | Same model, exposed per-deal for the Pipeline page |
| `generate_coaching_recommendations(rep_id)` | Rule/ML hybrid: finds the rep's weakest metric(s) vs. team benchmark and generates a text recommendation tied to it |
| `retrain_models(new_labeled_data)` | Batch job — retrains prediction model when enough new closed-deal data exists |

**Important build rule:** the AI service should never be called synchronously while a user waits on a page load for anything expensive (retraining, full sentiment reprocessing). Predictions and recommendations should be **pre-computed and stored**, then simply *read* by the dashboard.

---

## 5. Database Tables Needed (matches Appendix B of the PRD, plus AI Results)

| Table | Purpose |
|---|---|
| `users` | Auth + role |
| `customers` | Customer/company records |
| `deals` | Deal records + current stage/status |
| `activities` | Every logged sales action (call, email, meeting, note, stage-change) |
| `emails` | Raw emails + sentiment_score + tone |
| `ai_results` *(new)* | `deal_id`, `closing_probability`, `predicted_outcome`, `generated_at` |
| `recommendations` *(new)* | `rep_id`, `issue_text`, `metric_type`, `created_at` |
| `behaviour_metrics` *(new)* | `rep_id`, `period`, `avg_response_time`, `follow_up_frequency`, `behaviour_score` |

---

## 6. Feature Checklist (Build Order)

Use this as your literal task list — build top to bottom, each phase depends on the one before it.

**Phase 1 — Foundation**
- [ ] User auth (signup, login, JWT, role middleware)
- [ ] Customers CRUD
- [ ] Deals CRUD + stage tracking
- [ ] Activities logging

**Phase 2 — Communication Layer**
- [ ] Email upload + storage
- [ ] Sentiment analysis integration
- [ ] Tone detection integration

**Phase 3 — Analytics Layer**
- [ ] Response time calculation
- [ ] Follow-up frequency calculation
- [ ] Behaviour score computation
- [ ] Win/loss aggregation queries

**Phase 4 — Predictive Layer**
- [ ] Train deal-success prediction model on sample data
- [ ] Store closing probability per deal
- [ ] Build recommendation engine logic

**Phase 5 — Dashboard**
- [ ] Login/Signup pages
- [ ] Sales Performance page
- [ ] Pipeline Analytics page
- [ ] Win/Loss Analysis page
- [ ] Behaviour Analytics page
- [ ] Team Performance page
- [ ] Role-based routing/auth guard

**Phase 6 — Polish**
- [ ] Filters (date range, rep, team) wired to every page
- [ ] Loading/error states on every API call
- [ ] CI pipeline + tests

---

## 7. How a Typical User Session Should Actually Work

1. **Aditya (Rep)** logs in → lands on his personal Performance view (only his deals/metrics).
2. He opens a stalled deal, uploads the latest email thread → sentiment comes back negative.
3. Behaviour Analytics shows his response time is 5.4h (team avg 3.2h) → flagged red.
4. The AI Recommendation feed shows: *"Response time on 3 open deals exceeds the 4-hour benchmark — prioritize same-day replies."*
5. **Meera (Manager)** logs in → sees Team Performance → Aditya's card is flagged in the coaching queue.
6. She clicks into his Behaviour Analytics detail, sees the same data Aditya sees, and schedules a 1:1.
7. **Rohan (VP)** logs in weekly → sees org-wide Win/Loss trend and pipeline risk, no need to dig into individual reps unless something's flagged.

This is the loop the whole product exists to create: **data → insight → action → improved outcome**, visible to every role at the altitude they need.

---

## 8. What NOT to Build Yet (keep MVP scope tight)

Per the PRD's MVP boundaries, skip these until the core loop above works end-to-end:
- Salesforce/HubSpot sync
- Voice call analysis
- WhatsApp/chat analysis
- Real-time AI assistant/chatbot
- Mobile app
- Deep learning forecasting (classical ML is enough for MVP accuracy targets)

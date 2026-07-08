# SDET Automation Framework

A production-grade test automation framework built with Python, Selenium, pytest, and Docker.
Covers UI automation, API testing, database validation, and CI/CD integration across 7 projects.

**Author:** Sindhu Sundararajan  
**Target Roles:** SDET / QA Engineer — SS&C Technologies & Esri  
**Total Tests:** 29 passing across all projects

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| Selenium 4 | UI/browser automation |
| pytest | Test runner |
| pytest-html | HTML test reports |
| pytest-rerunfailures | Retry logic for flaky tests |
| requests | REST API testing |
| SQLite | Database validation (maps to MySQL/Snowflake) |
| Docker + Selenium Grid | Containerised test execution |
| Jenkins | CI/CD pipeline |
| Postman | Manual API verification |

---

## Project Structure

```
sdet_framework/
├── conftest.py                  # Shared fixtures — browser setup, screenshot on failure
├── Dockerfile                   # Container image for test execution
├── docker-compose.yml           # Selenium Grid + test container orchestration
├── Jenkinsfile                  # CI/CD pipeline with quality gate
├── requirements.txt             # Python dependencies
│
├── pages/                       # Page Object Model classes
│   ├── login_page.py            # Login page — locators + actions
│   └── inventory_page.py        # Inventory page — locators + actions + explicit waits
│
├── tests/                       # All test files
│   ├── test_login.py            # Project 1 — Login automation (5 tests)
│   ├── test_inventory.py        # Project 2 — POM + explicit waits (4 tests)
│   ├── test_login_DDT.py        # Project 3 — Data driven testing (5 tests)
│   └── test_api.py              # Project 4 — REST API testing (10 tests)
│
├── db_validation/               # Project 5 — Database validation
│   ├── create_db.py             # Creates SQLite test database
│   └── test_db.py               # ETL validation tests (5 tests)
│
└── reports/                     # Generated test reports and screenshots
    └── screenshots/             # Auto-captured on test failure
```

---

## Projects

### Project 1 — Login Automation (Selenium + POM)
**5 tests | `tests/test_login.py`**

Tests login scenarios on saucedemo.com using Page Object Model design pattern.

| Test | Scenario |
|---|---|
| test_valid_login | Standard user logs in successfully |
| test_locked_out_user | Locked user sees correct error |
| test_invalid_password | Wrong password shows error message |
| test_empty_username | Empty username shows validation error |
| test_empty_password | Empty password shows validation error |

**Key concepts:** pytest fixtures, conftest.py, POM, By.ID/CSS_SELECTOR/CLASS_NAME locators, implicit wait

---

### Project 2 — POM Framework + Explicit Waits
**4 tests | `tests/test_inventory.py`**

Extends Project 1 with a second page object and WebDriverWait for reliable element interaction.

| Test | Scenario |
|---|---|
| test_inventory_page | 6 products display after login |
| test_page_title | Products page title is correct |
| test_add_to_cart | Cart count increments after adding item |
| test_logout | Logout returns to login page |

**Key concepts:** WebDriverWait, ExpectedConditions, multi-page POM, race condition debugging

---

### Project 3 — Data Driven Testing
**5 tests | `tests/test_login_DDT.py`**

Replaces 5 separate test functions with one parametrized function — directly maps to the 80-days-to-5-days Cognizant resume story.

```python
@pytest.mark.parametrize("username, password, expected", [
    ("standard_user",  "secret_sauce",  "success"),
    ("locked_out_user","secret_sauce",  "locked out"),
    ("standard_user",  "secret_lab",    "do not match"),
    ("",               "secret_sauce",  "Username is required"),
    ("standard_user",  "",              "Password is required"),
])
```

**Key concepts:** parametrize, all-pair testing, conditional assert, data-driven design

---

### Project 4 — REST API Testing
**10 tests | `tests/test_api.py`**

Full CRUD coverage against JSONPlaceholder API using Python requests library.

| Test | Method | Endpoint | Validates |
|---|---|---|---|
| test_get_user_status_code | GET | /users/1 | Status 200 |
| test_get_user_data | GET | /users/1 | Payload integrity |
| test_get_user_response_time | GET | /users/1 | Response under 5s |
| test_get_invalid_user | GET | /users/999 | Status 404 |
| test_create_post | POST | /posts | Status 201 + data |
| test_get_all_users | GET | /users | 10 users returned |
| test_update_user | PUT | /users/1 | Full replace |
| test_patch_user | PATCH | /users/1 | Partial update |
| test_delete_user | DELETE | /users/1 | Empty response |
| test_get_user_schema | GET | /users/1 | All required fields exist |

**Key concepts:** requests.Session, GET/POST/PUT/PATCH/DELETE, schema validation, negative testing, response time assertion

---

### Project 5 — Database Validation
**5 tests | `db_validation/test_db.py`**

Validates ETL pipeline correctness using SQLite (maps to MySQL/Snowflake in production). Source table has 10 employees; destination loads only 8 active ones with a calculated bonus column.

| Test | What it validates |
|---|---|
| test_source_row_count | Source has exactly 10 records |
| test_destination_row_count | Destination has exactly 8 records |
| test_only_active_employees_loaded | Active source count matches destination count |
| test_salary_accuracy | Salary value preserved correctly through ETL |
| test_bonus_calculation | 10% bonus calculated and loaded correctly |

**Key concepts:** sqlite3, ETL validation, row count testing, data accuracy, schema compliance

---

### Project 6 — Docker + Selenium Grid + Jenkins CI/CD
**29 tests running in containers**

All tests run inside Docker using Selenium Grid for browser isolation.

```bash
# Run all tests in Docker
docker compose up --build
```

**Architecture:**
```
Jenkinsfile triggers → docker compose up
                            ↓
            chrome container (selenium/standalone-chrome)
                            ↑ HTTP
            tests container (Python + pytest)
                            ↓
                    HTML report generated
```

**Jenkins pipeline stages:** Build → Test → Quality Gate → Deploy → Report  
**Quality gate:** if any test fails, Deploy stage is blocked automatically

---

### Project 7 — Screenshot on Failure + Retry Logic
**Auto-captures browser state on failure | Auto-retries flaky tests**

**Screenshot on failure** — when any Selenium test fails, a screenshot is automatically saved to `reports/screenshots/{test_name}.png`. No manual intervention needed.

**Retry logic** — flaky tests are automatically retried up to 2 times with a 3-second delay before being marked as failed.

```bash
# Run with retry enabled
pytest tests/ -v --reruns 2 --reruns-delay 3 --html=reports/report.html --self-contained-html
```

---

## How to Run

### Prerequisites
- Python 3.12
- Chrome browser
- Docker Desktop (for containerised runs)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/sindhusundararajan/sdet_framework.git
cd sdet_framework

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run Individual Projects

```bash
# Project 1 — Login tests
pytest tests/test_login.py -v

# Project 2 — Inventory tests
pytest tests/test_inventory.py -v

# Project 3 — Data driven tests
pytest tests/test_login_DDT.py -v

# Project 4 — API tests
pytest tests/test_api.py -v

# Project 5 — Database tests
python db_validation/create_db.py
pytest db_validation/test_db.py -v
```

### Run Full Suite with Report

```bash
pytest tests/ -v --reruns 2 --reruns-delay 3 --html=reports/report.html --self-contained-html
```

### Run in Docker (Selenium Grid)

```bash
docker compose up --build
```

---

## Test Results

| Project | Tests | Result |
|---|---|---|
| 1 — Login Automation | 5 | ✅ PASSED |
| 2 — POM + Explicit Waits | 4 | ✅ PASSED |
| 3 — Data Driven Testing | 5 | ✅ PASSED |
| 4 — REST API Testing | 10 | ✅ PASSED |
| 5 — Database Validation | 5 | ✅ PASSED |
| 6 — Docker + Selenium Grid | 29 | ✅ PASSED |
| 7 — Screenshot + Retry | 24 | ✅ PASSED (1 rerun) |
| **Total** | **29** | **✅ ALL PASSING** |

---

## Key Design Decisions

**Page Object Model** — locators and actions live in page classes, not test files. When the UI changes, update one class — not 50 tests.

**Explicit over implicit waits** — `WebDriverWait` with `ExpectedConditions` waits for specific element states (clickable, visible) not just existence. Eliminates timing-based flakiness.

**Selenium Grid for Docker** — separates test runner from browser. Chrome runs in `selenium/standalone-chrome` container, solving WSL2 kernel compatibility issues and mirroring enterprise CI architecture.

**Schema validation** — API tests check field existence separately from field values. A broken API returning `{}` with status 200 passes value checks but fails schema validation.

**ETL validation pattern** — compare source active count against destination count rather than checking for absence of inactive records. Positive condition checks are always more reliable.
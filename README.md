# SDET Automation Framework

Python + Selenium + PyTest automation framework built across 7 projects.

## Project 1 — Login Automation (Selenium + POM)
- Page Object Model design pattern
- 5 login test scenarios (valid, locked out, invalid password, empty fields)
- pytest fixtures for browser setup and teardown
- HTML test reports via pytest-html

## Tech Stack
- Python 3.12
- Selenium 4
- PyTest
- WebDriver Manager
- Docker (coming soon)

## How to Run
```bash
pip install -r requirements.txt
pytest tests/test_login.py -v --html=reports/report.html --self-contained-html
```

## Test Results
5/5 tests passing 
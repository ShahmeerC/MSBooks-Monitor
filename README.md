# MSBooks Monitor

Automated inventory monitoring and analytics platform for educational book catalogs.

## Overview

MSBooks Monitor is a Python-based monitoring system that automatically tracks changes in an educational book catalog, detects additions, removals, and pricing updates, generates AI-powered summaries, sends notifications, and provides a web dashboard for historical analysis.

The system combines web scraping, automated monitoring, change detection, AI reporting, cloud deployment, and interactive data visualization into a single workflow.

---

## Features

### Automated Catalog Monitoring

* Scrapes and processes the latest catalog data
* Detects newly added books
* Detects removed books
* Detects price changes
* Maintains historical snapshots

### AI-Powered Reporting

* Generates monitoring summaries using LLMs
* Produces dashboard-ready insights
* Creates human-readable change reports

### Notifications

* Discord webhook alerts
* WhatsApp API integration support
* Automated cloud execution through GitHub Actions

### Analytics Dashboard

Built with Streamlit.

Includes:

* Inventory overview metrics
* Catalog exploration
* Search, filtering and sorting
* Inventory analytics and graphical visualizations
* Change details
* Historical inventory snapshots
* AI-generated reports

### Cloud Deployment

* Public dashboard deployment
* GitHub Actions automation
* Scheduled monitoring workflows
* Secure secret management

---

## Tech Stack

### Backend

* Python
* Pandas
* Requests
* BeautifulSoup
* Streamlit

### AI

* Groq API
* OpenAI API
* Google Gemini API

### Automation

* GitHub Actions
* Discord Webhooks
* WhatsApp Business API

---

## Project Structure

```text
dashboard/                 Streamlit dashboard
data/                      Catalog data and logs
data/history/              Historical snapshots

scraper.py                 Catalog scraper

weekly_monitor.py          Weekly change monitor
monthly_monitor.py         Monthly monitoring pipeline

weekly_stats.py            Weekly statistics
monthly_stats.py           Monthly statistics

AI_summaries.py            AI summary generation
```

---

## Monitoring Workflow

### Weekly Monitor

1. Scrape latest catalog
2. Compare against baseline
3. Detect changes
4. Generate summary
5. Send Discord notification
6. Update monitoring logs

### Monthly Monitor

1. Scrape latest catalog
2. Generate statistics
3. Detect additions/removals/pricing updates
4. Generate AI summaries
5. Save historical snapshot
6. Update dashboard data
7. Send notification

---

## Dashboard

Public deployment:

https://msbooks-monitor.streamlit.app

---

## Future Improvements

* Advanced dashboard analytics
* Database-backed storage
* Cloud infrastructure deployment
* Public API endpoints
* Enhanced notification channels
* Multi-catalog monitoring

---

## Author

Shahmeer Cornelius

Computer Engineering Student — GIKI

Focused on automation, data analysis, monitoring systems, AI-assisted workflows, and real-world software projects.

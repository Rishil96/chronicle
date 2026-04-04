# Change Log

All the notable changes to this project will be documented in this file

## v1.0.0 - (2026-04-04)

### Add
- SQLAlchemy ORM Model for Logs table
- Class to create database session for database operations
- Service layer functions that perform CRUD operations including add_log, get_logs, update_log, delete_log, get_log_by_id
- Logger configuration function to set up Singleton logger throughout the project
- FastAPI based web application with templates using HTML, HTMX, and Tailwind CSS having 3 web pages: home, history and filter.
- Utility functions to follow DRY principle
- Typer based CLI application with the following interfaces: add, today, filter, update, delete, history
- LLM class for integrating local and cloud based language models for log rephrasing and grammar correction

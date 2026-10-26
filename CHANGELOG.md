# Change Log

All the notable changes to this project will be documented in this file

## v2.0.0 - (2026-10-26)

### Add
- JWT based authentication with HTTP-only cookies, login and logout routes, and auth middleware that protects every route except login and static files
- Password hashing with bcrypt, and a change password page with validation
- Users, Topics and WorkUpdates ORM models with relationships, using timezone aware timestamps
- Alembic for database migrations, with the initial schema migration and a server default migration for work update timestamps
- pydantic-settings based configuration, with the database URL built from individual DB environment variables (PostgreSQL, SQL Server and SQLite supported)
- `scripts/create_user.py` to create user accounts from the terminal, since there is no public sign-up
- Work update form with a topic dropdown, topic description hint and markdown support for descriptions
- Add topic page with duplicate topic handling
- Home page with the logged in user's recent updates
- Updates page showing the whole team's updates grouped by date, newest first
- Filter page with a sidebar layout, filtering by user, topic, single date and date range
- Flash messages for success and error feedback across forms, including a session expired message
- Date mismatch check on the work update form, which keeps the typed text and asks the user to submit again
- Profile dropdown in the navbar with the user's initials, change password and logout
- Shared theme file with the brand color palette, and `static/.gitkeep` so a fresh clone starts

### Change
- Database moved from SQLite to PostgreSQL
- Work updates are now submitted under a topic with a single description, replacing one line logs
- Timestamps are stored in UTC and converted to IST on display and in date filters
- Color scheme changed to a darker blue
- Logger is now a single shared instance imported from `src.logger`
- Database session handling converted to a FastAPI dependency (`get_db`), and `create_all` replaced by Alembic migrations
- Auth redirects use 303 responses, and HTMX requests are redirected to login using the `HX-Redirect` header

### Remove
- Typer CLI tool and its global `chronicle` command
- LLM integration for log rephrasing
- v1 personal logs, with their routes, templates and services
- Editing and deleting of submitted updates
- Project, ProjectLogs and WorkCategories tables, merged into Topics


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

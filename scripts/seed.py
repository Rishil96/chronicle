import bcrypt
from src.db import get_db, Users, WorkCategories, Projects
from src.config import settings

print(f"Initialized testing environment setup using database from environment variables called: {settings.db_name}")

# Default password
default_password = "Chronicle@123"
password_hash = bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Get DB session
session = next(get_db())

# Create test user
test_user_id = 999
test_user = Users(
    id=test_user_id,
    first_name="Test",
    last_name="User",
    email="test@chronicle.com",
    password_hash=password_hash,
    is_admin=False
)
session.add(test_user)

# Add work categories
categories = ["R&D", "Meeting", "Bug Fix", "Code Review", "Deployment", "Documentation"]
for category in categories:
    session.add(WorkCategories(category_name=category))

# Add sample projects
projects = [
    Projects(project_name="Chronicle", client_name="Client A", description="Work log web application", created_by=test_user_id),
    Projects(project_name="Internal Tools", client_name="Client B", description="Internal team tools", created_by=test_user_id),
    Projects(project_name="Client Portal", client_name="Client C", description="Client facing portal", created_by=test_user_id),
]
for project in projects:
    session.add(project)

session.commit()
session.close()
print("Testing environment setup completed successfully!")

import bcrypt
from src.config import settings
from src.db import Topics, Users, get_db

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
    is_admin=True
)
session.add(test_user)

# Add topics
topics = {
    "R&D": "Use this to add updates on research work or learnings",
    "Meeting": "Use this to add meetings not related to a specific project",
    "Code Review": "Use this to add code review work update for projects not developed by us",
    "Documentation": "Use ths to add documentation updates for general tasks not specific to any project",
}

for topic_name, description in topics.items():
    session.add(Topics(topic_name=topic_name, description=description, created_by_id=test_user_id))

session.commit()
session.close()

print("Testing environment setup completed successfully!")

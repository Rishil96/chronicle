from fastapi.templating import Jinja2Templates

# Singleton object to render templates across all routes
templates = Jinja2Templates(directory="templates")

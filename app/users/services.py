from app.database import async_session
from app.users.models import User

from app.base import BaseService

class UserService(BaseService):
    model = User
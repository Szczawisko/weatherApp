from .models import User

class UserMenager:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user(id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

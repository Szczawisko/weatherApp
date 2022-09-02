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

    @staticmethod
    def save_user(data):
        User.objects.create_user(username=data["username"],password=data["password"])
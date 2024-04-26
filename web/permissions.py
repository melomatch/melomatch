from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from users.models import User


class CompareTastePermission(UserPassesTestMixin):
    def test_func(self):
        username = self.kwargs.get("username")

        if self.request.user.username == username:
            return False

        user_to_compare = get_object_or_404(User, username=username)
        return user_to_compare.is_active_link is True

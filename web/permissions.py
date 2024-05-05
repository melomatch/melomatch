from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from users.models import User


class CompareTastePermission(UserPassesTestMixin):
    def test_func(self):
        username = self.kwargs.get("username")
        by_query = self.request.GET.get("by")

        if self.request.user.username == username or by_query not in ["link", "search"]:
            return False

        user_to_compare = get_object_or_404(User, username=username)
        if by_query == "link":
            return user_to_compare.is_active_link is True
        return user_to_compare.is_private is False

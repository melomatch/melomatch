from django.forms import DateInput, EmailInput, ModelForm

from users.models import User


class BulmaFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr in self.fields:
            self.fields[attr].widget.attrs.update({"class": "input"})


class ProfileForm(BulmaFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "birthday", "sex")
        widgets = {
            "birthday": DateInput(attrs={"type": "date"}),
            "email": EmailInput(),
        }


class PrivacyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_private"].label = "Сделать аккаунт приватным?"
        self.fields["is_active_link"].label = "Активировать ссылку?"
        for attr in self.fields:
            self.fields[attr].widget.attrs.update(
                {"class": "switch is-rtl is-rounded is-outlined is-info"}
            )

    class Meta:
        model = User
        fields = ("is_private", "is_active_link")

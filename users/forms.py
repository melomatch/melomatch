from django.forms import DateInput, ModelForm

from users.models import User


class DefaultBulmaInputs:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr in self.fields:
            self.fields[attr].widget.attrs.update({"class": "input"})


class ProfileForm(DefaultBulmaInputs, ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "birthday", "sex")
        widgets = {
            "birthday": DateInput(attrs={"type": "date"}),
            "email": DateInput(attrs={"type": "email"}),
        }

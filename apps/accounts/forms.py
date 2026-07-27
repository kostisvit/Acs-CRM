from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Change labels
        self.fields["old_password"].label = "Τρέχον Κωδικός"
        self.fields["new_password1"].label = "Νέος Κωδικός"
        self.fields["new_password2"].label = "Επιβεβαίωση Κωδικού"

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-full px-4 py-3 border border-gray-300 "
                    "rounded-lg focus:ring-2 focus:ring-teal-500 "
                    "focus:border-teal-700 outline-none"
                )
            })
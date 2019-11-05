from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from django import forms


class UserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if self.cleaned_data.get('password2'):
            user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    # add_form = UserCreationForm
    list_display = ('id', 'name', 'username', 'last_login', 'is_active')
    search_fields = ('name', 'username')
    ordering = ('last_login',)
    list_filter = ('is_active', 'is_superuser')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

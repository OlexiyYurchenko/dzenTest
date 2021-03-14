from django import forms
from articles.models import Comments
from captcha.fields import CaptchaField
from articles.validators import validate_file_extension, validate_text_extension
# Create your forms here.

class CommentsForm(forms.ModelForm):
    captcha = CaptchaField(label='Are you an human?')
    user_name = forms.RegexField(regex = r'^[a-zA-Z0-9]+$', error_messages = {'invalid': ("Only symbols of the Latin alphabet, numbers (a–z, 0-9).")})
    img = forms.FileField(label='Img or txt', required=False, validators=[validate_file_extension])
    home_page = forms.URLField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=True, validators=[validate_text_extension])

    class Meta:
        model = Comments
        fields = ['user_name', 'email', 'home_page', 'img', 'text']

    def clean(self):
        cleaned_data = super(CommentsForm, self).clean()
        cleaned_data.pop('captcha', None)
        return cleaned_data


class CommentsFormPreview(forms.ModelForm):
    user_name = forms.RegexField(regex = r'^[a-zA-Z0-9]+$', error_messages = {'invalid': ("Only symbols of the Latin alphabet, numbers (a–z, 0-9).")})
    img = forms.FileField(label='Img or txt', required=False, validators=[validate_file_extension])
    home_page = forms.URLField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=True, validators=[validate_text_extension])

    class Meta:
        model = Comments
        fields = ['user_name', 'email', 'text', 'home_page', 'img']
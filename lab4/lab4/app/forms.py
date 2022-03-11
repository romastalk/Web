"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class AnketaForm(forms.Form):
    reviews_choice =(
        ("1", "Нормально"),
        ("2", "Хорошо"),
        ("3", "Отлично"),
    )
    
    list_reviews_choice=(
        ("1","Ничего"),
        ("2","Совсем ничего"),
        ("3","Всё хорошо"),
    )

    name = forms.CharField(label="Ваше имя", min_length=2, max_length=100)

    design = forms.ChoiceField(label="Как вам дизайн", 
                                choices= reviews_choice, 
                                widget=forms.RadioSelect,
                                initial=1)

    color_palette = forms.ChoiceField(label="Как вам цветовая палитра", 
                                choices= reviews_choice, 
                                widget=forms.RadioSelect,
                                initial=1)

    icon = forms.ChoiceField(label="Как вам иконка", 
                                choices= reviews_choice, 
                                widget=forms.RadioSelect,
                                initial=1)

    what_change = forms.ChoiceField(label="Что хотели бы изменить",
                                 choices=list_reviews_choice,
                                 initial=1)

    impressions = forms.CharField(label="Напишите остальные впечатления",
                                max_length=500,
                                widget=forms.Textarea(attrs={"rows":10, "cols":30}))

    visit = forms.BooleanField(label="Зашли бы снова?", required=False)   

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "description", "content", "image",)
        labels = {"title": "Заголовок", "description": "Краткое содержание", "content": "Полное содержание", "image": "Картинка"}





from django import forms
from .models import CustomUser
from .models import Game
from .models import Review, Tag

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GameUploadForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Выберите теги"
    )
    class Meta:
        model = Game
        fields = ['title', 'description', 'preview', 'game_file', 'tags']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
        }


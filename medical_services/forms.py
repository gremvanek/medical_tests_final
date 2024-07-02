from django import forms

from medical_services.models import Category


class CategoryForm(forms.ModelForm):
    """Форма для модели категорий"""

    class Meta:
        model = Category
        fields = ('name', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



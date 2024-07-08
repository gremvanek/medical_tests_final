from django import forms

from medical_services.models import Category, Service, Cart
from users.models import User


class CategoryForm(forms.ModelForm):
    """Форма для модели категорий"""

    class Meta:
        model = Category
        fields = ("name", "description", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ServiceForm(forms.ModelForm):
    """Форма для услуг"""

    class Meta:
        model = Service
        fields = ("name", "description", "image", "category", "price", "deadline")
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CartForm(forms.ModelForm):
    """Форма для модели корзины"""

    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Cart
        fields = ("client", "services", "date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = User.objects.filter(is_staff=False)  # Ограничение на выбор клиента
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

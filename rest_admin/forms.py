from django import forms
from .models import *
from accounts.models import User
from restaurant.models import OrderItem


class QrForm(forms.ModelForm):
    table_no = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Table
        fields = ['table_no']


class AddMenuForm(forms.ModelForm):

    Dish_Name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    Dish_Description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))
    speciality = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class': 'form-check-input',
        }))

    Price = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    pices = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = MenuTable
        exclude = ['res', 'status']
        widgets = {'category': forms.Select(attrs={'class': 'form-control'})}

    def __init__(self, user, *args, **kwargs):
        super(AddMenuForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.filter(
            rest_id=user)


class AddCategoryForm(forms.ModelForm):
    Category_Name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))
    Description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))

    class Meta:
        model = Categories
        fields = '__all__'
        exclude = ['rest']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password',
            'mobile_no', 'address', 'country', 'state', 'pin_code',
            'Adhaar_Card', 'Category', 'salary', 'profile_photo'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'pin_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Adhaar_Card': forms.FileInput(attrs={
                'class': '',
            }),
            'Category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'salary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': '',
            })
        }


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'mobile_no', 'address', 'country', 'state', 'pin_code',
            'Adhaar_Card', 'Category', 'salary', 'profile_photo'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'pin_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Adhaar_Card': forms.FileInput(attrs={
                'class': '',
            }),
            'Category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'salary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': '',
            })
        }


class ComForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = OrderItem
        fields = ['comment']

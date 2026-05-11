from django import forms
from .models import Client, Fournisseur

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone', 'adresse']
        # On ajoute des classes CSS pour que Django génère des inputs stylés
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du client'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemple@mail.com'}),
            'telephone': forms.TextInput(attrs={'placeholder': '+212...'}),
            'adresse': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adresse...'}),
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'email', 'telephone', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du fournisseur'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contact@fournisseur.com'}),
            'telephone': forms.TextInput(attrs={'placeholder': '+212...'}),
            'adresse': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adresse...'}),
        }
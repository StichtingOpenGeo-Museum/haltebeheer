from django import forms
from uni_form.helper import FormHelper
from uni_form.layout import Submit

class SearchForm(forms.Form):
    terms = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'placeholder' : 'Typ een zoekterm'}))
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = 'search'
        self.helper.form_class = 'nice'
        self.helper.add_input(Submit('submit', 'Zoek'))
        return super(SearchForm, self).__init__(*args, **kwargs)    
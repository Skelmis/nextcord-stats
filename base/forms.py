from django import forms


class SitemapFilterForm(forms.Form):
    filter_query = forms.CharField(max_length=25)

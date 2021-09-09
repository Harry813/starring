from django import forms
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from staring.text import *


class ContactForm(forms.Form):
    name = forms.CharField(
        min_length=2,
        label=ContactForm_name_text,
        widget=forms.TextInput(attrs={"placeholder": ContactForm_name_placeholder}),
        error_messages={
            "required": ContactForm_name_err_required
        }
    )

    email = forms.EmailField(
        label=ContactForm_email_text,
        widget=forms.EmailInput(attrs={"placeholder": ContactForm_email_placeholder})
    )

    contact_detail = forms.CharField(
        label=ContactForm_contact_text,
        widget=forms.TextInput(
            attrs={"placeholder": ContactForm_contact_placeholder}
        )
    )

    query = forms.CharField(
        label=ContactForm_query_text,
        widget=forms.Textarea(
            attrs={"placeholder": ContactForm_query_placeholder}
        )
    )

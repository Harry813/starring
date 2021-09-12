from django import forms
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from staring.text import *
from staring.models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ["name", "email", "contact_detail", "query"]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": consult_name_placeholder})
        self.fields["email"].widget.attrs.update({"placeholder": consult_email_placeholder})
        self.fields["contact_detail"].widget.attrs.update({"placeholder": consult_contact_placeholder})
        self.fields["query"].widget.attrs.update({"placeholder": consult_query_placeholder})

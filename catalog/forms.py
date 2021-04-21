import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

RENEWAL_WEEKS_AHEAD = 4

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check that the date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check that the date is within the allowed range
        if data > datetime.date.today() + datetime.timedelta(weeks=RENEWAL_WEEKS_AHEAD):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data


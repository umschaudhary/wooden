from django import forms

from refunds.models import RefundPolicy, RefundRequest


class RefundPolicyForm(forms.ModelForm):
    class Meta:
        model = RefundPolicy
        fields = [
            'validity',
            'cover',
            'description',
            'type_acceptance'
        ]


class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = [
            'quantity'
        ]

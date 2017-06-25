from django import forms
from .models import *


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['name', 'description']


class ContinuousRuleForm(forms.ModelForm):
    class Meta:
        model = ContinuousRule
        fields = ['name', 'midi_cc', 'continuous_param', 'scale_down', 'scale_up']


class StandardRuleForm(forms.ModelForm):
    class Meta:
        model = StandardRule
        fields = ['name', 'note', 'event_param', 'max_duration']


class BankRuleForm(forms.ModelForm):
    class Meta:
        model = BankRule
        fields = ['name', 'max_duration']


class ChaseRuleForm(forms.ModelForm):
    class Meta:
        model = ChaseRule
        fields = ['name', 'event_param', 'state_duration', 'random_states']


class BankRuleStateForm(forms.ModelForm):
    class Meta:
        model = BankRuleState
        fields = ['name', 'note', 'priority']


class ChaseRuleStateForm(forms.ModelForm):
    class Meta:
        model = ChaseRuleState
        fields = ['name', 'note']


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['bool_param', 'bool_active_on_false', 'continuous_param', 'operator', 'value']
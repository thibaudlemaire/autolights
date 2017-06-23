from django.db import models

# LedWall config model
class Configuration(models.Model):
    name = models.CharField(max_length=100, null=True)         # Configuration's name
    description = models.TextField(null=True)       # If necessary, add a description
    creation = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Creation")
    modification = models.DateTimeField(auto_now_add=False, auto_now=True,
                                verbose_name="Modification")

    def __str__(self):
        return self.name


class ContinuousRule(models.Model):
    name = models.CharField(max_length=100)         # Rule's name
    config = models.ForeignKey('Configuration')     # Configuration the rule belong to
    midi_cc = models.IntegerField()                 # Midi control to link
    scale_down = models.IntegerField()              # Setting full scale
    scale_up = models.IntegerField()

    def __str__(self):
        return self.name


class StandardRule(models.Model):
    name = models.CharField(max_length=100, null=True)  # Rule's name
    config = models.ForeignKey('Configuration')         # Configuration the rule belong to
    note = models.IntegerField()                        # Midi note
    event_id = models.IntegerField()                    # Event type ID
    duration = models.IntegerField()                    # Note duration in ms
    note_off = models.BooleanField()                    # Set to send note_off after

    def __str__(self):
        return self.name


class StandardRuleCondition(models.Model):
    rule = models.ForeignKey('StandardRule')        # Rule's the condition belongs to
    param_id = models.IntegerField()                # Id of the param to check
    inferior = models.BooleanField()                # Operator to apply
    superior = models.BooleanField()
    equal = models.BooleanField()
    value = models.IntegerField()                   # Value to compare with


class BankRule(models.Model):
    name = models.CharField(max_length=100)         # Rule's name
    config = models.ForeignKey('Configuration')     # Configuration the rule belong to
    max_duration_beats = models.IntegerField()      # Max duration of a state

    def __str__(self):
        return self.name


class BankRuleState(models.Model):
    name = models.CharField(max_length=100)         # State name
    rule = models.ForeignKey('BankRule')            # Rule this action belongs to
    note = models.IntegerField()                    # Midi note
    priority = models.IntegerField                  # Priority between 1 to 100

    def __str__(self):
        return self.name


class BankRuleStateCondition(models.Model):
    rule = models.ForeignKey('BankRuleState')       # State's the condition belongs to
    param_id = models.IntegerField()                # Id of the param to check
    inferior = models.BooleanField()                # Operator to apply
    superior = models.BooleanField()
    equal = models.BooleanField()
    value = models.IntegerField()                   # Value to compare with


class ChaseRule(models.Model):
    name = models.CharField(max_length=100)         # Rule's name
    config = models.ForeignKey('Configuration')     # Configuration the rule belong to
    event_id = models.IntegerField                  # Trigger event ID
    duration_beats = models.IntegerField()          # Duration of a state
    random_states = models.BooleanField()           # Set state order to random

    def __str__(self):
        return self.name


class ChaseRuleState(models.Model):
    name = models.CharField(max_length=100)         # State name
    rule = models.ForeignKey('ChaseRule')           # Rule this action belongs to
    note = models.IntegerField()                    # Midi note

    def __str__(self):
        return self.name


class ChaseRuleStateCondition(models.Model):
    rule = models.ForeignKey('ChaseRuleState')      # State's the condition belongs to
    param_id = models.IntegerField()                # Id of the param to check
    inferior = models.BooleanField()                # Operator to apply
    superior = models.BooleanField()
    equal = models.BooleanField()
    value = models.IntegerField()                   # Value to compare with

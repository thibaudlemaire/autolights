from django.db import models

# Configuration
#   - ContinuousRule
#   - StandardRule
#       - StandardRuleCondition
#   - BankRule
#       - BankRuleState
#           - BankRuleStateCondition
#   - ChaseRule
#       - ChaseRuleState


# LedWall config model
class Configuration(models.Model):
    name = models.CharField(max_length=100, null=True)  # Configuration's name
    description = models.TextField(null=True)           # If necessary, add a description
    creation = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Creation")
    modification = models.DateTimeField(auto_now_add=False, auto_now=True,
                                verbose_name="Modification")

    def __str__(self):
        return self.name


# Rules

class Rule(models.Model):
    name = models.CharField(max_length=100)             # Rule's name
    config = models.ForeignKey('Configuration')         # Configuration the rule belong to

    class Meta:
        abstract = True


class ContinuousRule(Rule):
    midi_cc = models.IntegerField()                     # Midi control to link
    continuous_param = models.ForeignKey('ContinuousParam')        # Param to link
    scale_down = models.IntegerField()                  # Setting full scale
    scale_up = models.IntegerField()

    def __str__(self):
        return self.name


class StandardRule(Rule):
    note = models.IntegerField()                        # Midi note
    event_param = models.ForeignKey('EventParam')       # Triggering event, if null checks on condition change
    max_duration = models.IntegerField(default=0)       # Note duration in ms, 0 --> infinite

    def __str__(self):
        return self.name


class BankRule(Rule):
    max_duration = models.IntegerField(null=True)       # Max duration of a state

    def __str__(self):
        return self.name


class ChaseRule(Rule):
    event_param = models.ForeignKey('EventParam')       # Triggering event
    state_duration = models.IntegerField()              # Duration of a state
    random_states = models.BooleanField()               # Set state order to random

    def __str__(self):
        return self.name


# Conditions

class Condition(models.Model):
    # Boolean condition
    bool_param = models.ForeignKey('BoolParam', null=True, blank=True)
    bool_active_on_false = models.BooleanField(default=False)
    # Continuous condition
    continuous_param = models.ForeignKey('ContinuousParam', null=True, blank=True)
    operator = models.CharField(
        max_length=3,
        choices=(('<', '<'),('=', '='),('>', '>')),
        default='<')
    value = models.IntegerField(null=True, blank=True)                                      # Value to compare with

    class Meta:
        abstract = True

    def __str__(self):
        if self.bool_param: return self.bool_param.name
        else: return str(self.continuous_param) + self.operator + str(self.value)


class StandardRuleCondition(Condition):
    rule = models.ForeignKey('StandardRule')            # Rule's the condition belongs to


class BankRuleStateCondition(Condition):
    rule = models.ForeignKey('BankRuleState')           # State's the condition belongs to


class ChaseRuleCondition(Condition):
    rule = models.ForeignKey('ChaseRule')               # State's the condition belongs to


# States

class State(models.Model):
    name = models.CharField(max_length=100)  # State name
    note = models.IntegerField()  # Midi note

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BankRuleState(State):
    rule = models.ForeignKey('BankRule')                # Rule this action belongs to
    priority = models.IntegerField()                    # Priority between 1 to 100


class ChaseRuleState(State):
    rule = models.ForeignKey('ChaseRule')               # Rule this action belongs to


# Parameters

class Param(models.Model):
    name = models.CharField(max_length=100)             # Param name

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class EventParam(Param):
    None


class ContinuousParam(Param):
    None


class BoolParam(Param):
    None

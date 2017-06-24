from django.contrib import admin
from .models import Configuration, ContinuousRule, StandardRule, BankRule, ChaseRule, \
    BankRuleStateCondition, ChaseRuleCondition, StandardRuleCondition, BankRuleState, ChaseRuleState, \
   EventParam, ContinuousParam, BoolParam


class ConfigurationAdmin(admin.ModelAdmin):
   list_display   = ('name', 'description')
   list_filter    = 'name'
   date_hierarchy = 'creation'
   ordering       = 'creation'
   search_fields  = ('name', 'description')

admin.site.register(Configuration)
admin.site.register(ContinuousRule)
admin.site.register(StandardRule)
admin.site.register(BankRule)
admin.site.register(ChaseRule)
admin.site.register(BankRuleState)
admin.site.register(BankRuleStateCondition)
admin.site.register(ChaseRuleCondition)
admin.site.register(StandardRuleCondition)
admin.site.register(ChaseRuleState)
admin.site.register(EventParam)
admin.site.register(BoolParam)
admin.site.register(ContinuousParam)

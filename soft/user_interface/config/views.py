from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .forms import *


def list_config(request):
    date = datetime.now()
    configs = Configuration.objects.all()
    return render(request, 'config/list-config.html', locals())


def add_config(request):
    config = Configuration(name='New configuration', description='', active=False)
    config.save()
    return edit_config(request, config.id)


def del_config(request, id):
    get_object_or_404(Configuration, id=id).delete()
    return redirect('list-config')


def edit_config(request, id):
    config = get_object_or_404(Configuration, id=id)
    form = ConfigurationForm(request.POST or None, instance=config)
    if form.is_valid():
        config = form.save()
        success_message = "Configuration " + config.name + " modified successfully."
        return render_config(request, config=config, success_message=success_message, form=form)
    else:
        return render_config(request, config=config, form=form)


def active_config(request, id):
    config = get_object_or_404(Configuration, id=id)
    config.active = True
    config.save()
    return redirect('list-config')


def render_config(request, config, form=None, success_message=None):
    if not form:
        form = ConfigurationForm(instance=config)
    continuous_rules = ContinuousRule.objects.filter(config=config)
    standard_rules = StandardRule.objects.filter(config=config)
    bank_rules = BankRule.objects.filter(config=config)
    chase_rules = ChaseRule.objects.filter(config=config)
    return render(request, 'config/edit-config.html', locals())


def home(request):
    return render(request, 'config/home.html')


def edit_continuous_rule(request, id):
    rule = get_object_or_404(ContinuousRule, id=id)
    config = rule.config
    form = ContinuousRuleForm(request.POST or None, instance=rule)
    if form.is_valid():
        rule = form.save()
        success_message = "Continuous rule " + rule.name + " modified successfully."
        return render_config(request, success_message=success_message, config=config)
    else:
        form = ContinuousRuleForm(instance=rule)
        return render(request, 'config/edit-continuous-rule.html', locals())


def edit_standard_rule(request, id):
    rule = get_object_or_404(StandardRule, id=id)
    config = rule.config
    # Form processing
    form = StandardRuleForm(request.POST or None, instance=rule)
    if form.is_valid():
        rule = form.save()
        success_message = "Standard rule " + rule.name + " modified successfully."
        return render_config(request, success_message=success_message, config=config)
    else:
        form = StandardRuleForm(instance=rule)
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-standard-rule.html', locals())


def edit_bank_rule(request, id):
    rule = get_object_or_404(BankRule, id=id)
    config = rule.config
    # Form processing
    form = BankRuleForm(request.POST or None, instance=rule)
    condition_form = False
    if form.is_valid():
        rule = form.save()
        success_message = "Bank rule " + rule.name + " modified successfully."
        form = BankRuleForm(instance=rule)
        form_state = BankRuleStateForm()
        add_state = True
        return render(request, 'config/edit-bank-rule.html', locals())
    else:
        form = BankRuleForm(instance=rule)
        form_state = BankRuleStateForm()
        add_state = True
        return render(request, 'config/edit-bank-rule.html', locals())


def edit_chase_rule(request, id):
    rule = get_object_or_404(ChaseRule, id=id)
    config = rule.config
    # Form processing
    form = ChaseRuleForm(request.POST or None, instance=rule)
    form_cond = ConditionForm()
    add_cond = True
    if form.is_valid():
        rule = form.save()
        success_message = "Chase rule " + rule.name + " modified successfully."
        form = ChaseRuleForm(instance=rule)
        form_state = ChaseRuleStateForm()
        add_state = True
        return render(request, 'config/edit-chase-rule.html', locals())
    else:
        form = ChaseRuleForm(instance=rule)
        form_state = ChaseRuleStateForm()
        add_state = True
        return render(request, 'config/edit-chase-rule.html', locals())


def del_continuous_rule(request, id):
    rule = get_object_or_404(ContinuousRule, id=id)
    config = rule.config
    rule.delete()
    success_message = "Continuous rule " + rule.name + " deleted successfully."
    return render_config(request, success_message=success_message, config=config)


def del_standard_rule(request, id):
    rule = get_object_or_404(StandardRule, id=id)
    config = rule.config
    rule.delete()
    success_message = "Standard rule " + rule.name + " deleted successfully."
    return render_config(request, success_message=success_message, config=config)


def del_bank_rule(request, id):
    rule = get_object_or_404(BankRule, id=id)
    config = rule.config
    rule.delete()
    success_message = "Bank rule " + rule.name + " deleted successfully."
    return render_config(request, success_message=success_message, config=config)


def del_chase_rule(request, id):
    rule = get_object_or_404(ChaseRule, id=id)
    config = rule.config
    rule.delete()
    success_message = "Chase rule " + rule.name + " deleted successfully."
    return render_config(request, success_message=success_message, config=config)


def add_continuous_rule(request, config_id):
    config = get_object_or_404(Configuration, id=config_id)
    if request.POST:
        form = ContinuousRuleForm(request.POST or None)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.config = config
            rule.save()
            success_message = "Continuous rule " + rule.name + " created successfully."
            return render_config(request, success_message=success_message, config=config)
    else:
        form = ContinuousRuleForm()
        add = True
        return render(request, 'config/edit-continuous-rule.html', locals())


def add_standard_rule(request, config_id):
    config = get_object_or_404(Configuration, id=config_id)
    if request.POST:
        form = StandardRuleForm(request.POST or None)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.config = config
            rule.save()
            success_message = "Standard rule " + rule.name + " created successfully."
            return render_config(request, success_message=success_message, config=config)
    else:
        form = StandardRuleForm()
        add = True
        return render(request, 'config/edit-standard-rule.html', locals())


def add_bank_rule(request, config_id):
    config = get_object_or_404(Configuration, id=config_id)
    condition_form = False
    form_state = BankRuleStateForm()
    add_state = True
    if request.POST:
        form = BankRuleForm(request.POST or None)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.config = config
            rule.save()
            success_message = "Bank rule " + rule.name + " created successfully."
            return render_config(request, success_message=success_message, config=config)
    else:
        form = BankRuleForm()
        add = True
        return render(request, 'config/edit-bank-rule.html', locals())


def add_chase_rule(request, config_id):
    config = get_object_or_404(Configuration, id=config_id)
    if request.POST:
        form = ChaseRuleForm(request.POST or None)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.config = config
            rule.save()
            success_message = "Chase rule " + rule.name + " created successfully."
            return render_config(request, success_message=success_message, config=config)
    else:
        form = ChaseRuleForm()
        add = True
        return render(request, 'config/edit-chase-rule.html', locals())


def add_bank_rule_state(request, rule_id):
    rule = get_object_or_404(BankRule, id=rule_id)
    form = BankRuleForm(instance=rule)
    condition_form = False
    config = rule.config
    if request.POST:
        form_state = BankRuleStateForm(request.POST or None)
        if form_state.is_valid():
            state = form_state.save(commit=False)
            state.rule = rule
            state.save()
            success_message = "Bank rule state " + state.name + " created successfully."
            form_state = BankRuleStateForm()
            add_state = True
            return render(request, 'config/edit-bank-rule.html', locals())
    else:
        form_state = BankRuleStateForm()
        add_state = True
        return render(request, 'config/edit-bank-rule.html', locals())


def add_chase_rule_state(request, rule_id):
    rule = get_object_or_404(ChaseRule, id=rule_id)
    form = ChaseRuleForm(instance=rule)
    form_cond = ConditionForm()
    add_cond = True
    config = rule.config
    if request.POST:
        form_state = ChaseRuleStateForm(request.POST or None)
        if form_state.is_valid():
            state = form_state.save(commit=False)
            state.rule = rule
            state.save()
            success_message = "Chase rule state " + state.name + " created successfully."
            form_state = ChaseRuleStateForm()
            add_state = True
            return render(request, 'config/edit-chase-rule.html', locals())
    else:
        form_state = ChaseRuleStateForm()
        add_state = True
        return render(request, 'config/edit-chase-rule.html', locals())


def edit_bank_rule_state(request, state_id):
    state = get_object_or_404(BankRuleState, id=state_id)
    rule = state.rule
    form = BankRuleForm(instance=rule)
    condition_form = False
    config = rule.config
    if request.POST:
        form_state = BankRuleStateForm(request.POST or None, instance=state)
        if form_state.is_valid():
            state = form_state.save()
            success_message = "Bank rule state " + state.name + " modified successfully."
            form_state = BankRuleStateForm()
            add_state = True
            return render(request, 'config/edit-bank-rule.html', locals())
    else:
        form_state = BankRuleStateForm(instance=state)
        add_state = False
        return render(request, 'config/edit-bank-rule.html', locals())


def edit_chase_rule_state(request, state_id):
    state = get_object_or_404(ChaseRuleState, id=state_id)
    rule = state.rule
    form = ChaseRuleForm(instance=rule)
    form_cond = ConditionForm()
    add_cond = True
    config = rule.config
    if request.POST:
        form_state = ChaseRuleStateForm(request.POST or None, instance=state)
        if form_state.is_valid():
            state = form_state.save()
            success_message = "Chase rule state " + state.name + " modified successfully."
            form_state = ChaseRuleStateForm()
            add_state = True
            return render(request, 'config/edit-chase-rule.html', locals())
    else:
        form_state = ChaseRuleStateForm(instance=state)
        add_state = False
        return render(request, 'config/edit-chase-rule.html', locals())


def del_bank_rule_state(request, state_id):
    state = get_object_or_404(BankRuleState, id=state_id)
    rule = state.rule
    config = rule.config
    state.delete()
    success_message = "Bank rule state " + state.name + " deleted successfully."
    form = BankRuleForm(instance=rule)
    form_state = BankRuleStateForm()
    add_state = True
    condition_form = False
    return render(request, 'config/edit-bank-rule.html', locals())


def del_chase_rule_state(request, state_id):
    state = get_object_or_404(ChaseRuleState, id=state_id)
    rule = state.rule
    config = rule.config
    state.delete()
    success_message = "Chase rule state " + state.name + " deleted successfully."
    form = ChaseRuleForm(instance=rule)
    form_state = ChaseRuleStateForm()
    form_cond = ConditionForm()
    add_cond = True
    add_state = True
    return render(request, 'config/edit-chase-rule.html', locals())


def add_standard_rule_condition(request, rule_id):
    rule = get_object_or_404(StandardRule, id=rule_id)
    config = rule.config
    condition = StandardRuleCondition()
    # Form processing
    form = StandardRuleForm(instance=rule)
    form_cond = ConditionForm(request.POST or None, instance=condition)
    if form_cond.is_valid():
        condition = form_cond.save(commit=False)
        condition.rule = rule
        condition.save()
        success_message = "Condition added successfully."
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-standard-rule.html', locals())
    else:
        form = StandardRuleForm(instance=rule)
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-standard-rule.html', locals())


def add_chase_rule_condition(request, rule_id):
    rule = get_object_or_404(ChaseRule, id=rule_id)
    config = rule.config
    condition = ChaseRuleCondition()
    # Form processing
    form = ChaseRuleForm(instance=rule)
    form_state = ChaseRuleStateForm()
    add_state = True
    form_cond = ConditionForm(request.POST or None, instance=condition)
    if form_cond.is_valid():
        condition = form_cond.save(commit=False)
        condition.rule = rule
        condition.save()
        success_message = "Condition added successfully."
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-chase-rule.html', locals())
    else:
        form = ChaseRuleForm(instance=rule)
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-chase-rule.html', locals())


def add_bank_rule_state_condition(request, state_id):
    state = get_object_or_404(BankRuleState, id=state_id)
    rule = state.rule
    config = rule.config
    condition = BankRuleStateCondition()
    # Form processing
    form = BankRuleForm(instance=rule)
    form_state = BankRuleStateForm()
    add_state = True
    form_cond = ConditionForm(request.POST or None, instance=condition)
    if form_cond.is_valid():
        condition = form_cond.save(commit=False)
        condition.state = state
        condition.save()
        success_message = "Condition added successfully."
        condition_form = False
        return render(request, 'config/edit-bank-rule.html', locals())
    else:
        form = BankRuleForm(instance=rule)
        form_cond = ConditionForm()
        add_cond = True
        condition_form = True
        return render(request, 'config/edit-bank-rule.html', locals())


def edit_standard_rule_condition(request, condition_id):
    condition = get_object_or_404(StandardRuleCondition, id=condition_id)
    rule = condition.rule
    config = rule.config
    # Form processing
    form = StandardRuleForm(instance=rule)
    form_cond = ConditionForm(request.POST or None, instance=condition)
    if form_cond.is_valid():
        condition = form_cond.save()
        success_message = "Condition modified successfully."
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-standard-rule.html', locals())
    else:
        form = StandardRuleForm(instance=rule)
        form_cond = ConditionForm(instance=condition)
        add_cond = False
        return render(request, 'config/edit-standard-rule.html', locals())


def edit_chase_rule_condition(request, condition_id):
    condition = get_object_or_404(ChaseRuleCondition, id=condition_id)
    rule = condition.rule
    config = rule.config
    # Form processing
    form = ChaseRuleForm(instance=rule)
    form_state = ChaseRuleStateForm()
    add_state = True
    form_cond = ConditionForm(request.POST or None, instance=condition)
    if form_cond.is_valid():
        condition = form_cond.save()
        success_message = "Condition modified successfully."
        form_cond = ConditionForm()
        add_cond = True
        return render(request, 'config/edit-chase-rule.html', locals())
    else:
        form_cond = ConditionForm(instance=condition)
        add_cond = False
        return render(request, 'config/edit-chase-rule.html', locals())


def edit_bank_rule_state_condition(request, condition_id):
    condition = get_object_or_404(BankRuleStateCondition, id=condition_id)
    state = condition.state
    rule = state.rule
    config = rule.config
    # Form processing
    form = BankRuleForm(instance=rule)
    form_state = BankRuleStateForm()
    add_state = True
    form_cond = ConditionForm(request.POST or None, instance=condition)
    if form_cond.is_valid():
        condition = form_cond.save()
        success_message = "Condition modified successfully."
        condition_form = False
        return render(request, 'config/edit-bank-rule.html', locals())
    else:
        form_cond = ConditionForm(instance=condition)
        add_cond = False
        condition_form = True
        return render(request, 'config/edit-bank-rule.html', locals())

def del_standard_rule_condition(request, condition_id):
    condition = get_object_or_404(StandardRuleCondition, id=condition_id)
    rule = condition.rule
    config = rule.config
    condition.delete()
    success_message = "Condition deleted successfully."
    form = StandardRuleForm(instance=rule)
    form_cond = ConditionForm()
    add_cond = True
    return render(request, 'config/edit-standard-rule.html', locals())


def del_chase_rule_condition(request, condition_id):
    condition = get_object_or_404(ChaseRuleCondition, id=condition_id)
    rule = condition.rule
    config = rule.config
    condition.delete()
    success_message = "Condition deleted successfully."
    form = ChaseRuleForm(instance=rule)
    form_cond = ConditionForm()
    form_state = ChaseRuleStateForm()
    add_cond = True
    add_state = True
    return render(request, 'config/edit-chase-rule.html', locals())


def del_bank_rule_state_condition(request, condition_id):
    condition = get_object_or_404(BankRuleStateCondition, id=condition_id)
    state = condition.state
    rule = state.rule
    config = rule.config
    condition.delete()
    success_message = "Condition deleted successfully."
    form = BankRuleForm(instance=rule)
    form_state = BankRuleStateForm()
    add_state = True
    condition_form = False
    return render(request, 'config/edit-bank-rule.html', locals())
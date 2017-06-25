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
        return render(request, 'config/edit-standard-rule.html', locals())


def edit_bank_rule(request, id):
    rule = get_object_or_404(BankRule, id=id)
    config = rule.config
    # Form processing
    form = BankRuleForm(request.POST or None, instance=rule)
    if form.is_valid():
        rule = form.save()
        success_message = "Bank rule " + rule.name + " modified successfully."
        return render_config(request, success_message=success_message, config=config)
    else:
        form = BankRuleForm(instance=rule)
        return render(request, 'config/edit-bank-rule.html', locals())


def edit_chase_rule(request, id):
    rule = get_object_or_404(ChaseRule, id=id)
    config = rule.config
    # Form processing
    form = ChaseRuleForm(request.POST or None, instance=rule)
    if form.is_valid():
        rule = form.save()
        success_message = "Chase rule " + rule.name + " modified successfully."
        return render_config(request, success_message=success_message, config=config)
    else:
        form = ChaseRuleForm(instance=rule)
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
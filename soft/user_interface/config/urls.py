from django.conf.urls import url
import config.views


urlpatterns = [
    url(r'^$', config.views.home, name='home'),
    url(r'^list-config$', config.views.list_config, name='list-config'),
    url(r'^edit-config/([0-9]+)$', config.views.edit_config, name='edit-config'),
    url(r'^add-config$', config.views.add_config, name='add-config'),
    url(r'^del-config/([0-9]+)$', config.views.del_config, name='del-config'),
    url(r'^active-config/([0-9]+)$', config.views.active_config, name='active-config'),
    url(r'^edit-continuous-rule/([0-9]+)$', config.views.edit_continuous_rule, name='edit-continuous-rule'),
    url(r'^edit-standard-rule/([0-9]+)$', config.views.edit_standard_rule, name='edit-standard-rule'),
    url(r'^edit-bank-rule/([0-9]+)$', config.views.edit_bank_rule, name='edit-bank-rule'),
    url(r'^edit-chase-rule/([0-9]+)$', config.views.edit_chase_rule, name='edit-chase-rule'),
    url(r'^config/([0-9]+)/add-continuous-rule$', config.views.add_continuous_rule, name='add-continuous-rule'),
    url(r'^config/([0-9]+)/add-standard-rule$', config.views.add_standard_rule, name='add-standard-rule'),
    url(r'^config/([0-9]+)/add-bank-rule$', config.views.add_bank_rule, name='add-bank-rule'),
    url(r'^config/([0-9]+)/add-chase-rule$', config.views.add_chase_rule, name='add-chase-rule'),
    url(r'^del-continuous-rule/([0-9]+)$', config.views.del_continuous_rule, name='del-continuous-rule'),
    url(r'^del-standard-rule/([0-9]+)$', config.views.del_standard_rule, name='del-standard-rule'),
    url(r'^del-bank-rule/([0-9]+)$', config.views.del_bank_rule, name='del-bank-rule'),
    url(r'^del-chase-rule/([0-9]+)$', config.views.del_chase_rule, name='del-chase-rule'),
]
r'^articles/(?P<year>\d{4})/(?P<month>\d{2})$'
from django.conf.urls import url
import config.views


urlpatterns = [
    url(r'^$', config.views.home, name='home'),
    url(r'^list-config$', config.views.list_config, name='list-config'),
    url(r'^edit-config/([0-9]+)$', config.views.edit_config, name='edit-config'),
    url(r'^edit-continuous-rule/([0-9]+)$', config.views.edit_continuous_rule, name='edit-continuous-rule'),

]

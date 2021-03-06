from django.views.generic import TemplateView
from edc_base.view_mixins import AdministrationViewMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class AdministrationView(EdcBaseViewMixin, NavbarViewMixin,
                         AdministrationViewMixin, TemplateView):

    navbar_name = 'esr21'
    navbar_selected_item = 'administration'

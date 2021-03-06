import configparser
from datetime import datetime
import os

from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.management.color import color_style
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_data_manager.apps import AppConfig as BaseEdcDataManagerAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_label.apps import AppConfig as BaseEdcLabelAppConfig
from edc_locator.apps import AppConfig as BaseEdcLocatorAppConfig
from edc_meddra.apps import AppConfig as BaseEdcMeddraAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
from edc_timepoint.timepoint import Timepoint
from edc_timepoint.timepoint_collection import TimepointCollection

from edc_appointment.appointment_config import AppointmentConfig
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_appointment.constants import COMPLETE_APPT
from edc_senaite_interface.apps import AppConfig as BaseEdcSenaiteInterfaceAppConfig
from edc_sync.apps import AppConfig as BaseEdcSyncAppConfig
from edc_sync_files.apps import AppConfig as BaseEdcSyncFilesAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT, \
    COMPLETED_PROTOCOL_VISIT, MISSED_VISIT
from esr21_dashboard.patterns import subject_identifier

style = color_style()

config = configparser.RawConfigParser()
config.read(os.path.join(settings.ETC_DIR,
                         settings.CONFIG_FILE))


class AppConfig(DjangoAppConfig):
    name = 'esr21'


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    configurations = [
        AppointmentConfig(
            model='edc_appointment.appointment',
            related_visit_model='esr21_subject.subjectvisit',
            appt_type='clinic'),
    ]


class EdcDataManagerAppConfig(BaseEdcDataManagerAppConfig):
    identifier_pattern = subject_identifier
    assianable_users_note = True
    email_issue_notification = False
    extra_assignee_choices = {
        'gabs_clinic': [
            ('gabs_clinic', 'AZD Gababorone Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'maun_clinic': [
            ('maun_clinic', 'AZD Maun Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'serowe_clinic': [
            ('serowe_clinic', 'AZD Serowe Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'gheto_clinic': [
            ('gheto_clinic', 'AZD Francistown Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'sphikwe_clinic': [
            ('sphikwe_clinic', 'AZD Selibe Phikwe Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'se_dmc': [
            ('se_dmc', 'SE & Data Management'),
            ['adiphoko@bhp.org.bw', 'ckgathi@bhp.org.bw', 'imosweu@bhp.org.bw',
             'mmotlhanka@bhp.org.bw', 'mchawawa@bhp.org.bw', 'nmunatsi@bhp.org.bw']]}


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'BHP150'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    report_datetime_allowance = -1
    visit_models = {
        'esr21_subject': ('subject_visit', 'esr21_subject.subjectvisit'), }


class EdcLabAppConfig(BaseEdcLabAppConfig):
    requisition_model = 'esr21_subject.subjectrequisition'
    result_model = 'edc_lab.result'


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = 'botswana'
    definitions = {
        '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[100, 100, 100, 100, 100, 100, 100]),
        '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                             slots=[100, 100, 100, 100, 100])}


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP150'
    protocol_name = 'BHP150 | ADZ 1222 - ESR-21-21311'
    protocol_number = '150'
    protocol_title = ''
    study_open_datetime = datetime(
        2021, 4, 1, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(
        2025, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
    timepoints = TimepointCollection(
        timepoints=[
            Timepoint(
                model='edc_appointment.appointment',
                datetime_field='appt_datetime',
                status_field='appt_status',
                closed_status=COMPLETE_APPT),
            Timepoint(
                model='edc_appointment.historicalappointment',
                datetime_field='appt_datetime',
                status_field='appt_status',
                closed_status=COMPLETE_APPT),
        ])


class EdcLocatorAppConfig(BaseEdcLocatorAppConfig):
    name = 'edc_locator'
    reference_model = 'esr21_subject.personalcontactinfo'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {
        'esr21_subject.subjectvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED, COMPLETED_PROTOCOL_VISIT]
    delete_on_reasons = [LOST_VISIT, MISSED_VISIT, FAILED_ELIGIBILITY]


class EdcSenaiteInterfaceAppConfig(BaseEdcSenaiteInterfaceAppConfig):
    host = "https://bhplims.bhp.org.bw"
    client = "AZD1222"
    courier = "ABRAHAM MAIGWA"
    sample_type_match = {'humoral_immunogenicity': 'Serum',
                         'sars_serum': 'Serum',
                         'sars_cov2_pcr': 'Swab',
                         'hematology': 'Whole Blood EDTA',
                         'wb_cmi': 'Whole Blood EDTA',
                         'urine_hcg': 'Urine'}
    container_type_match = {'humoral_immunogenicity': 'Cryogenic vial',
                            'sars_cov2_serology': 'Cryogenic vial',
                            'sars_cov2_pcr': 'Cryogenic Vial',
                            'hematology': 'EDTA Tube',
                            'wb_cmi': 'EDTA Tube',
                            'urine_hcg': 'Urine Cup'}
    template_match = {'humoral_immunogenicity': 'Serum storage',
                      'sars_serum': 'SARS-CoV-2 serology',
                      'sars_cov2_pcr': 'SARS COV 2 PCR',
                      'hematology': 'CBC',
                      'wb_cmi': 'PBMC Whole Blood EDTA',
                      'urine_hcg': 'Urine HCG'}


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    use_settings = True
    device_id = settings.DEVICE_ID
    device_role = settings.DEVICE_ROLE
    node_server_id_list = ['94', '95', '96', '97', '98']


class EdcLabelAppConfig(BaseEdcLabelAppConfig):
    template_folder = os.path.join(
        settings.STATIC_ROOT, 'esr21', 'label_templates')


class EdcSyncAppConfig(BaseEdcSyncAppConfig):
    edc_sync_files_using = True
    server_ip = config['edc_sync'].get('server_ip')
    base_template_name = 'esr21/base.html'


class EdcSyncFilesAppConfig(BaseEdcSyncFilesAppConfig):
    edc_sync_files_using = True
    remote_host = config['edc_sync_files'].get('remote_host')
    user = config['edc_sync_files'].get('sync_user')
    usb_volume = config['edc_sync_files'].get('usb_volume')
    remote_media = config['edc_sync_files'].get('remote_media')
    tmp_folder = os.path.join(remote_media, 'transactions', 'tmp')
    incoming_folder = os.path.join(remote_media, 'transactions', 'incoming')
    media_path = os.path.join(settings.MEDIA_ROOT, 'other_media')
    media_dst = os.path.join(remote_media)
    media_tmp = os.path.join('/tmp/')

    def make_required_folders(self):
        """Makes all folders declared in the config if they
        do not exist.
        """
        client_folders = [self.outgoing_folder, self.archive_folder]

        server_folders = [self.incoming_folder, self.archive_folder,
                          self.tmp_folder, self.pending_folder,
                          self.log_folder]

        folder_dict = {'Client': client_folders,
                       'CentralServer': server_folders,
                       'NodeServer': server_folders}

        role = config['edc_device'].get('role')

        for folder in folder_dict.get(role):
            if not os.path.exists(folder):
                os.makedirs(folder)


class EdcMeddraAppConfig(BaseEdcMeddraAppConfig):
    version = 24.1
    ctcae_version = 5.0

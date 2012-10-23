#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2012 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase
from common.utils import BaseAuthenticatedClient
from dialer_cdr.models import Callrequest, VoIPCall
from dialer_cdr.forms import VoipSearchForm
from dialer_cdr.views import export_voipcall_report, voipcall_report,\
                             voipcall_report_grid
from dialer_cdr.function_def import voipcall_search_admin_form_fun
from dialer_cdr.tasks import init_callrequest, \
                             dummy_testcall, \
                             dummy_test_answerurl, \
                             dummy_test_hangupurl
from utils.helper import grid_test_data
from datetime import datetime


class DialerCdrView(BaseAuthenticatedClient):
    """Test cases for Callrequest, VoIPCall Admin Interface."""

    def test_admin_callrequest_view_list(self):
        """Test Function to check admin callrequest list"""
        response = self.client.get('/admin/dialer_cdr/callrequest/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_callrequest_view_add(self):
        """Test Function to check admin callrequest add"""
        response = self.client.get('/admin/dialer_cdr/callrequest/add/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.post(
            '/admin/dialer_cdr/callrequest/add/',
            data={'status': '1', 'campaign': '1',
                  'aleg_uuid': 'e8fee8f6-40dd-11e1-964f-000c296bd875',
                  'callerid': '12345',
                  'request_uuid': 'e8fee8f6-40dd-11e1-964f-000c296bd875',
                  'phone_number': '123456789',
                  'aleg_gateway': '1',
                  'user': '1'})
        self.assertEqual(response.status_code, 200)

    def test_admin_voipcall_view_list(self):
        """Test Function to check admin voipcall list"""
        response = self.client.get('/admin/dialer_cdr/voipcall/')
        self.failUnlessEqual(response.status_code, 200)

    def test_admin_voipcall_view_report(self):
        """Test Function to check admin voipcall list"""
        response = self.client.get('/admin/dialer_cdr/voipcall/voip_report/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.post('/admin/dialer_cdr/voipcall/voip_report/',
            data={'from_date': datetime.now().strftime("%Y-%m-%d"),
                  'to_date': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(
            '/admin/dialer_cdr/voipcall/voip_report/',
            data={'from_date': datetime.now().strftime("%Y-%m-%d"),
                  'to_date': datetime.now().strftime("%Y-%m-%d")})
        request.user = self.user
        request.session = {}
        response = voipcall_search_admin_form_fun(request)
        self.assertTrue(response)


class DialerCdrCustomerView(BaseAuthenticatedClient):
    """Test cases for Callrequest, VoIPCall Customer Interface."""

    def test_customer_voipcall(self):
        """Test Function to check VoIP call report"""
        request = self.factory.post('/voipcall_report_grid/', grid_test_data)
        request.user = self.user
        request.session = {}
        response = voipcall_report_grid(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(
            '/voipcall_report_grid/?from_date=&disposition=1',
            grid_test_data)
        request.user = self.user
        request.session = {}
        response = voipcall_report_grid(request)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/voipcall_report/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'], VoipSearchForm())
        self.assertTemplateUsed(response,
            'frontend/report/voipcall_report.html')

        response = self.client.post('/voipcall_report/',
                        data={'from_date': datetime.now().strftime("%Y-%m-%d"),
                              'to_date': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('/voipcall_report/')
        request.user = self.user
        request.session = {}
        response = voipcall_report(request)
        self.assertEqual(response.status_code, 200)

    def test_export_voipcall_report(self):
        """Test Function to check VoIP call export report"""
        request = self.factory.get('/export_voipcall_report/')
        request.user = self.user
        request.session = {}
        request.session['voipcall_record_qs'] = {}
        response = export_voipcall_report(request)
        self.assertEqual(response.status_code, 200)


class DialerCdrCeleryTaskTestCase(TestCase):
    """Test cases for celery task"""

    fixtures = ['gateway.json', 'voiceapp.json', 'auth_user.json',
                'dialer_setting.json', 'contenttype.json',
                'phonebook.json', 'contact.json',
                'campaign.json', 'subscriber.json',
                'callrequest.json', 'voipcall.json', 'user_profile.json']

    def setUp(self):
        self.callrequest = Callrequest.objects.get(pk=1)

    #def test_init_callrequest(self):
    #    """Test that the ``init_callrequest``
    #    task runs with no errors, and returns the correct result."""
    #    result = init_callrequest.delay(self.callrequest.id, 1)
    #    self.assertEqual(result.successful(), True)

    def test_dummy_test_answerurl(self):
        """Test that the ``dummy_test_answerurl``
        task runs with no errors, and returns the correct result."""
        result = dummy_test_answerurl.delay(self.callrequest.request_uuid)
        self.assertEqual(result.successful(), True)

    def test_dummy_test_hangupurl(self):
        """Test that the ``dummy_test_hangupurl``
        periodic task runs with no errors, and returns the correct result."""
        result = dummy_test_hangupurl.delay(self.callrequest.request_uuid)
        self.assertEqual(result.successful(), True)


class DialerCdrModel(TestCase):
    """Test Callrequest, VoIPCall models"""

    fixtures = ['gateway.json', 'auth_user.json', 'contenttype.json',
                'phonebook.json', 'contact.json',
                'campaign.json', 'subscriber.json',
                'callrequest.json', 'survey.json', 'section.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')

        try:
            content_type_id = ContentType.objects.get(model='voiceapp').id
        except:
            content_type_id = 1

        # Callrequest model
        self.callrequest = Callrequest(
            call_type=1,
            status=1,
            user=self.user,
            phone_number='123456',
            subscriber_id=1,
            campaign_id=1,
            aleg_gateway_id=1,
            content_type_id=content_type_id,
            object_id=1,
        )
        self.callrequest.save()

        # VoIPCall model
        self.voipcall = VoIPCall(
            user=self.user,
            used_gateway_id=1,
            callrequest=self.callrequest,
            callid='Top Gun',
            phone_number='123456',
            leg_type=1,
            duration=20,
        )
        self.voipcall.save()
        self.assertEqual(self.voipcall.__unicode__(), u'1 - Top Gun')

        # Test mgt command
        call_command("create_callrequest_cdr", "1|1")

        call_command("create_callrequest_cdr", "3|1")

    def test_name(self):
        self.assertEqual(self.callrequest.phone_number, "123456")
        #self.assertEqual(self.callrequest.__unicode__(), u'Top Gun')
        self.assertEqual(self.voipcall.phone_number, "123456")

        Callrequest.objects.get_pending_callrequest()

        self.voipcall.destination_name()
        self.voipcall.duration = ''
        self.voipcall.min_duration()
        self.voipcall.duration = 12
        self.voipcall.min_duration()

    def teardown(self):
        self.callrequest.delete()
        self.voipcall.delete()

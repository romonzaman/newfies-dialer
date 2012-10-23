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

from django.test import TestCase
from common.utils import BaseAuthenticatedClient
from frontend.forms import LoginForm, DashboardForm
from frontend.views import customer_dashboard, index, \
                           login_view, logout_view, pleaselog

from newfies.urls import custom_404_view, custom_500_view


class FrontendView(BaseAuthenticatedClient):
    """Test cases for Newfies-Dialer Admin Interface."""

    def test_admin(self):
        """Test Function to check Admin index page"""
        response = self.client.get('/admin/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/base_site.html')
        response = self.client.login(username=self.user.username,
                                     password='admin')
        self.assertEqual(response, True)


class FrontendCustomerView(BaseAuthenticatedClient):
    """Test cases for Newfies-Dialer Customer Interface."""

    fixtures = ['dialer_setting.json', 'auth_user.json', 'gateway.json',
                'voiceapp.json', 'phonebook.json', 'contact.json',
                'campaign.json', 'subscriber.json',
                'callrequest.json', 'voipcall.json']


    def test_login_view(self):
        """Test Function to check login view"""
        response = self.client.post('/login/',
                {'user': 'admin',
                 'password': 'admin'}, follow=True)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/login/',
                {'user': 'admin',
                 'password': 'admin'}, follow=True)
        request.user = self.user
        request.session = self.client.session
        response = login_view(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.post('/login/',
                {'user': '', 'password': ''}, follow=True)
        request.user = self.user
        request.session = self.client.session
        response = login_view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/login/',
                {'user': 'admin', 'password': 'admin123'}, follow=True)
        request.user = self.user
        request.session = self.client.session
        response = login_view(request)
        self.assertEqual(response.status_code, 200)

    def test_pleaselog(self):
        """Test Function to check pleaselog view"""
        response = self.client.get('/pleaselog/')
        self.assertTemplateUsed(response, 'frontend/index.html')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        """Test Function to check customer index page"""
        response = self.client.get('/')
        self.assertTrue(response.context['loginform'], LoginForm())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/index.html')


        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        """Test Function to check customer dashboard"""
        response = self.client.get('/dashboard/')
        self.assertTrue(response.context['form'], DashboardForm(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/dashboard.html')

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '1',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '2',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '3',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '4',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '5',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '6',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/dashboard/',
                {'campaign': '1',
                 'search_type': '7',
                 'call_count_button': 'true',
                 'duration_button': 'true'})

        request.user = self.user
        request.session = {}
        response = customer_dashboard(request)
        self.assertEqual(response.status_code, 200)
        response = customer_dashboard(request, on_index='yes')


    def test_logout_view(self):
        """Test Function to check logout view"""
        response = self.client.post('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/logout/', follow=True)
        request.user = self.user
        request.session = self.client.session
        request.LANGUAGE_CODE = 'en'
        response = logout_view(request)
        self.assertEqual(response.status_code, 302)

    def test_custom_404_view(self):
        request = self.factory.post('/logout/')
        request.user = self.user
        request.session = {}
        response = custom_404_view(request)
        self.assertEqual(response.status_code, 500)

    def test_custom_500_view(self):
        """Test Function to check 500_view"""
        request = self.factory.post('/xyz/')
        request.user = self.user
        request.session = {}
        response = custom_500_view(request)
        self.assertEqual(response.status_code, 500)


class FrontendForgotPassword(TestCase):
    """Test cases for Newfies-Dialer Customer Interface. for forgot password"""

    def test_check_password_reset(self):
        """Test Function to check password reset"""
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'frontend/registration/password_reset_form.html')
        response = self.client.post('/password_reset/',
                                    {'email': 'admin@localhost.com'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/password_reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'frontend/registration/password_reset_done.html')

        response = self.client.get('/reset/1-2xc-5791af4cc6b67e88ce8e/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'frontend/registration/password_reset_confirm.html')
        response = self.client.post('/reset/1-2xc-5791af4cc6b67e88ce8e/',
                                    {'new_password1': 'admin',
                                     'new_password2': 'admin' },
                                    follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'frontend/registration/password_reset_complete.html')

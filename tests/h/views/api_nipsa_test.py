# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from pyramid.httpexceptions import HTTPNoContent, HTTPNotFound

from h.views import api_nipsa as views


@pytest.mark.usefixtures('nipsa_service', 'has_permission')
class TestCreate(object):
    def test_it_creates_the_nipsa_flag(self, pyramid_request, resource, nipsa_service):
        views.create(resource, pyramid_request)

        nipsa_service.create.assert_called_once_with(resource.annotation)

    def test_it_renders_no_content(self, pyramid_request, resource):
        response = views.create(resource, pyramid_request)
        assert isinstance(response, HTTPNoContent)

    def test_it_checks_for_group_admin_permission(self, pyramid_request, resource):
        views.create(resource, pyramid_request)
        pyramid_request.has_permission.assert_called_once_with('admin', resource.group)

    def test_it_responds_with_not_found_when_no_admin_access_in_group(self, pyramid_request, resource):
        pyramid_request.has_permission.return_value = False
        with pytest.raises(HTTPNotFound):
            views.create(resource, pyramid_request)

    @pytest.fixture
    def resource(self):
        return mock.Mock(spec_set=['annotation', 'group'])

    @pytest.fixture
    def nipsa_service(self, pyramid_config):
        svc = mock.Mock(spec_set=['create'])
        pyramid_config.register_service(svc, name='annotation_nipsa')
        return svc

    @pytest.fixture
    def has_permission(self, pyramid_request):
        func = mock.Mock(return_value=True)
        pyramid_request.has_permission = func
        return func

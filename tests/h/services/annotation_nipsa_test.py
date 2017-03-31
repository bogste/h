# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from h import models
from h.services.annotation_nipsa import AnnotationNipsaService
from h.services.annotation_nipsa import annotation_nipsa_service_factory


class TestAnnotationNipsaServiceCreate(object):
    def test_it_creates_annotation_nipsa(self, svc, factories, db_session):
        annotation = factories.Annotation()
        svc.create(annotation)

        nipsa = db_session.query(models.AnnotationNipsa) \
                          .filter_by(annotation=annotation) \
                          .first()

        assert nipsa is not None

    def test_it_skips_creating_nipsa_when_already_exists(self, svc, factories, db_session):
        existing = factories.AnnotationNipsa()

        svc.create(existing.annotation)

        count = db_session.query(models.AnnotationNipsa) \
                          .filter_by(annotation=existing.annotation) \
                          .count()

        assert count == 1

    @pytest.fixture
    def svc(self, db_session):
        return AnnotationNipsaService(db_session)


class TestAnnotationNipsaServiceFactory(object):
    def test_it_returns_service(self, pyramid_request):
        svc = annotation_nipsa_service_factory(None, pyramid_request)
        assert isinstance(svc, AnnotationNipsaService)

    def test_it_provides_request_db_as_session(self, pyramid_request):
        svc = annotation_nipsa_service_factory(None, pyramid_request)
        assert svc.session == pyramid_request.db

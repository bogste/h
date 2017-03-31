# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from h import models


class AnnotationNipsaService(object):
    def __init__(self, session):
        self.session = session

    def create(self, annotation):
        """
        Create an annotation nipa flag.

        This hides the given annotation from anybody except its author and the
        group moderators.

        In case the given annotation already has a nipsa flag, this method
        is a no-op.

        :param annotation: The annotation to hide from others.
        :type annotation: h.models.Annotation
        """

        query = self.session.query(models.AnnotationNipsa) \
                            .filter_by(annotation=annotation)

        if query.count() > 0:
            return

        nipsa = models.AnnotationNipsa(annotation=annotation)
        self.session.add(nipsa)


def annotation_nipsa_service_factory(context, request):
    return AnnotationNipsaService(request.db)

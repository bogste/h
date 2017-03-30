# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sqlalchemy as sa

from memex.db import types

from h.db import Base
from h.db.mixins import Timestamps


class AnnotationNipsa(Base, Timestamps):
    """
    A nipsa flag for an individual annotation.

    This means that the annotation is violating the community guidelines and
    should be hidden from other users.
    """

    __tablename__ = 'annotation_nipsa'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    annotation_id = sa.Column(types.URLSafeUUID,
                              sa.ForeignKey('annotation.id', ondelete='cascade'),
                              nullable=False)

    #: The annotation which has been flagged.
    annotation = sa.orm.relationship('Annotation')

    def __repr__(self):
        return '<AnnotationNipsa annotation_id=%s>' % self.annotation_id

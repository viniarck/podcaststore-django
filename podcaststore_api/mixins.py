#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mixins.
"""

from django.utils.timezone import now


class ValidateOnSaveMixin:
    """Mixin to always enforce validation on save."""

    def save(self, force_insert=False, force_update=False, full_clean=True, **kwargs):
        """Save overwrite."""
        if full_clean:
            self.full_clean()
        # if hasattr(self, "modificado_em"):
        #     self.modificado_em = now()
        super().save(force_insert, force_update, **kwargs)  # type: ignore

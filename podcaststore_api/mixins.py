#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mixins.
"""


class ValidateOnSaveMixin:
    """Mixin to always enforce validation on save."""

    def save(self, force_insert=False, force_update=False, full_clean=True, **kwargs):
        """Save overwrite."""
        if full_clean:
            self.full_clean()
        super().save(force_insert, force_update, **kwargs)  # type: ignore

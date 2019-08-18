#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from podcaststore_api.models.reaction import Reaction, ReactionSerializer
from typing import Dict, Any


class TestReactionModel:

    """TestReactionModel."""

    @pytest.mark.django_db
    def test_repr(
        self, create_reaction: Reaction, reaction_data: Dict[str, Any]
    ) -> None:
        """Test __repr__ method."""
        reaction = create_reaction
        assert repr(reaction) == f"Reaction({reaction.id}, {reaction_data['code']})"


class TestTagSerializer:

    """TestTagSerializer"""

    @pytest.mark.django_db
    def test_ser_data(self, reaction_data: Dict[str, Any]) -> None:
        """Test serialization data."""
        reaction_serd = ReactionSerializer(data=reaction_data)
        assert reaction_serd.is_valid()
        for field in ("code",):
            assert field in reaction_serd.data

    @pytest.mark.django_db
    def test_ser_data_save(
        self, create_reaction: Reaction, reaction_data: Dict[str, Any]
    ) -> None:
        """Test serialization data with save."""
        reaction_data["user_id"] = create_reaction.user_id
        reaction_data["track_id"] = create_reaction.track_id
        reaction = Reaction(**reaction_data)
        reaction.save()
        reaction_serd = ReactionSerializer(reaction)
        for field in ReactionSerializer.Meta.fields:
            assert field in reaction_serd.data

    @pytest.mark.django_db
    def test_ser_invalid(self, reaction_data: Dict[str, Any]) -> None:
        """Test serialization invalid data."""
        del reaction_data["code"]
        reaction_serd = ReactionSerializer(data=reaction_data)
        assert not reaction_serd.is_valid()
        assert "code" in reaction_serd.errors

    @pytest.mark.django_db
    def test_ser_invalid_code(self, reaction_data: Dict[str, Any]) -> None:
        """Test serialization invalid data."""
        reaction_data["code"] = "foo"
        reaction_serd = ReactionSerializer(data=reaction_data)
        assert not reaction_serd.is_valid()
        assert "code" in reaction_serd.errors

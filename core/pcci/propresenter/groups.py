"""Mapping detected sections onto ProPresenter groups.

Read out of the reference export (docs/FORMAT_NOTES.md §4.6):

* every occurrence of a section is its own ``CueGroup`` with its own ``Group.uuid``;
* a section that recurs reuses the same name and colour, and the arrangement lists it
  again rather than inventing "Chorus 3";
* numbered variants are darkened;
* ``application_group_identifier`` points at a workspace preset. We cannot know the
  UUIDs of somebody else's workspace, so ours is left empty — exactly as the
  user-created "Post Chorus" group in the reference file does.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from pcci.config import RGBA, ConversionConfig
from pcci.ir import Section, SectionType

#: Hot keys ProPresenter itself assigned in the reference file. Groups it left without
#: one (Interlude, Post Chorus, Vamp) get 0, which is "no hot key".
DEFAULT_HOT_KEYS: dict[SectionType, int] = {
    SectionType.VERSE: 1,
    SectionType.BRIDGE: 2,
    SectionType.CHORUS: 3,
    SectionType.INTRO: 9,
}


@dataclass(frozen=True, slots=True)
class GroupIdentity:
    """What one section becomes in the presentation."""

    name: str
    colour: RGBA
    hot_key: int
    key: tuple[SectionType, int | None, str]


@dataclass
class GroupAssigner:
    """Hands out group identities, reusing one per distinct section."""

    config: ConversionConfig
    _identities: dict[tuple[SectionType, int | None, str], GroupIdentity] = field(
        default_factory=dict
    )

    def identity_for(self, section: Section) -> GroupIdentity:
        key = (section.type, section.number, section.variant)
        existing = self._identities.get(key)
        if existing is not None:
            return existing
        identity = GroupIdentity(
            name=section.label,
            colour=self.config.colour_for(section.type, section.number),
            hot_key=DEFAULT_HOT_KEYS.get(section.type, 0),
            key=key,
        )
        self._identities[key] = identity
        return identity


def new_uuid() -> str:
    """A fresh UUIDv4 in the upper-case form ProPresenter writes."""
    return str(uuid.uuid4()).upper()

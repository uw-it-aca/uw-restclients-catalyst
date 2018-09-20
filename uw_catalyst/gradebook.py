"""
Interface for interacting with Catalyst GradeBook
"""

from uw_catalyst.models import GradebookParticipant
from uw_catalyst.exceptions import InvalidGradebookID
from uw_catalyst import get_resource, encode_section_label
import re


def get_participants_for_gradebook(gradebook_id, person=None):
    """
    Returns a list of gradebook participants for the passed gradebook_id and
    person.
    """
    if not valid_gradebook_id(gradebook_id):
        raise InvalidGradebookID(gradebook_id)

    url = "/rest/gradebook/v1/book/{}/participants".format(gradebook_id)
    headers = {}

    if person is not None:
        headers["X-UW-Act-as"] = person.uwnetid

    data = get_resource(url, headers)

    participants = []
    for pt in data["participants"]:
        participants.append(_participant_from_json(pt))

    return participants


def get_participants_for_section(section, person=None):
    """
    Returns a list of gradebook participants for the passed section and person.
    """
    section_label = encode_section_label(section.section_label())
    url = "/rest/gradebook/v1/section/{}/participants".format(section_label)
    headers = {}

    if person is not None:
        headers["X-UW-Act-as"] = person.uwnetid

    data = get_resource(url, headers)

    participants = []
    for pt in data["participants"]:
        participants.append(_participant_from_json(pt))

    return participants


def valid_gradebook_id(gradebook_id):
    if re.match(r"^[1-9][0-9]{,9}$", str(gradebook_id)):
        return True
    return False


def _participant_from_json(data):
    participant = GradebookParticipant()
    participant.participant_id = data["participant_id"]
    participant.class_grade = data["class_grade"]
    participant.notes = data["notes"]
    participant.person_id = data["person_id"]
    return participant

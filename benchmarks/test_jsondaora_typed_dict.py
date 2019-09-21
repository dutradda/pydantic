from dataclasses import field
from datetime import datetime
from typing import List, Optional, TypedDict

from jsondaora import asdataclass, jsondaora, string, integer
from jsondaora.exceptions import DeserializationError


class TestTypingJsonTypedDict:
    package = 'jsondaora-typed-dict'

    def __init__(self, allow_extra):

        @jsondaora
        class Model(TypedDict):
            id: int
            client_name: string(max_length=255)
            # client_name: str
            sort_index: float
            grecaptcha_response: string(min_length=20, max_length=1000)
            # client_email: EmailStr = None
            client_phone: string(max_length=255) = None

            @jsondaora
            class Location(TypedDict):
                latitude: Optional[float] = None
                longitude: Optional[float] = None
            location: Optional[Location] = None

            contractor: integer(minimum=0) = None
            upstream_http_referrer: string(max_length=1023) = None
            last_updated: datetime = None

            @jsondaora
            class Skill(TypedDict):
                subject: str
                subject_id: int
                category: str
                qual_level: str
                qual_level_id: int
                qual_level_ranking: float = .0
            skills: List[Skill] = field(default_factory=list)

        self.allow_extra = allow_extra  # unused
        self.model = Model

    def validate(self, data):
        try:
            return True, asdataclass(data, self.model)
        except DeserializationError as e:
            # print(e)
            return False, str(e)

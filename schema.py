from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class TrackEnum(str, Enum):
    SOFTWARE_ENGINEERING = "software_engineering"
    AI_ML = "ai_ml"
    DATA_ANALYTICS = "data_analytics"
    PRODUCT_DESIGN = "product_design"
    UNKNOWN = "unknown"


class AvailabilityEnum(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    WEEKENDS_ONLY = "weekends_only"
    UNSPECIFIED = "unspecified"


class InternshipApplication(BaseModel):
    applicant_name: Optional[str] = Field(
        default=None,
        description="Full name of the applicant if explicitly stated; otherwise null."
    )
    email: Optional[str] = Field(
        default=None,
        description="Applicant email address if present; otherwise null."
    )
    track: TrackEnum = Field(
        default=TrackEnum.UNKNOWN,
        description="Target internship track mapped to allowed enum values."
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of technical or domain skills mentioned."
    )
    availability: AvailabilityEnum = Field(
        default=AvailabilityEnum.UNSPECIFIED,
        description="Preferred work schedule/availability."
    )
    years_of_experience: float = Field(
        default=0.0,
        ge=0.0,
        le=30.0,
        description="Estimated years of relevant experience (0.0 if student/entry-level)."
    )
    is_complete: bool = Field(
        default=False,
        description="True only if applicant_name, email, and a non-unknown track are provided."
    )
    missing_fields: List[str] = Field(
        default_factory=list,
        description="List of required fields that were missing or unclear in the input."
    )

    @field_validator("skills")
    @classmethod
    def clean_skills(cls, v: List[str]) -> List[str]:
        return [skill.strip().lower() for skill in v if skill and skill.strip()]
import os
import re
from typing import Any, Dict, Tuple
from dotenv import load_dotenv
from pydantic import ValidationError

from prompts import SYSTEM_PROMPT_V1, SYSTEM_PROMPT_V2, USER_PROMPT_TEMPLATE
from schema import AvailabilityEnum, InternshipApplication, TrackEnum

load_dotenv()


def _detect_track(text_lower: str) -> TrackEnum:
    if any(k in text_lower for k in ["machine learning", "ai", "llm", "nlp", "pytorch", "tensorflow"]):
        return TrackEnum.AI_ML
    if any(k in text_lower for k in ["data analyst", "analytics", "tableau", "power bi", "sql", "pandas"]):
        return TrackEnum.DATA_ANALYTICS
    if any(k in text_lower for k in ["ui", "ux", "figma", "product design", "wireframe"]):
        return TrackEnum.PRODUCT_DESIGN
    if any(k in text_lower for k in ["backend", "frontend", "fullstack", "software", "fastapi", "django", "react", "javascript"]):
        return TrackEnum.SOFTWARE_ENGINEERING
    return TrackEnum.UNKNOWN


def _detect_availability(text_lower: str) -> AvailabilityEnum:
    if "full-time" in text_lower or "full time" in text_lower:
        return AvailabilityEnum.FULL_TIME
    if "part-time" in text_lower or "part time" in text_lower:
        return AvailabilityEnum.PART_TIME
    if "weekend" in text_lower:
        return AvailabilityEnum.WEEKENDS_ONLY
    return AvailabilityEnum.UNSPECIFIED


def _detect_skills(text_lower: str) -> list[str]:
    known_skills = [
        "python", "javascript", "typescript", "react", "fastapi", "flask",
        "django", "sql", "git", "docker", "figma", "excel", "pandas", "c++"
    ]
    return [skill for skill in known_skills if re.search(rf"\b{re.escape(skill)}\b", text_lower)]


def _detect_experience(text_lower: str) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)", text_lower)
    if match:
        return float(match.group(1))
    return 0.0


def _detect_email(text: str) -> str | None:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None


def _detect_name(text: str, version: str) -> str | None:
    patterns = [
        r"(?:i am|i'm|my name is|name is)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
    ]
    for pat in patterns:
        match = re.search(pat, text, flags=re.IGNORECASE if "name is" in pat or "i'm" in pat or "i am" in pat else 0)
        if match:
            candidate = " ".join(part.capitalize() for part in match.group(1).strip().split())
            if candidate.lower() not in {"ignore previous", "system prompt", "hello there", "api key"}:
                return candidate
    return None

    


def extract_application(raw_text: Any, version: str = "v2") -> Tuple[bool, Dict[str, Any], str]:
    """
    Extracts structured data and validates it against InternshipApplication.
    Returns: (is_valid, payload_dict, message)
    """
    _ = SYSTEM_PROMPT_V2 if version == "v2" else SYSTEM_PROMPT_V1
    _ = USER_PROMPT_TEMPLATE.format(raw_text=str(raw_text))

    if not isinstance(raw_text, str) or not raw_text.strip():
        return False, {}, "Invalid input: expected a non-empty text string."

    text_lower = raw_text.lower()
    name = _detect_name(raw_text, version=version)
    email = _detect_email(raw_text)
    track = _detect_track(text_lower)
    skills = _detect_skills(text_lower)
    availability = _detect_availability(text_lower)
    years_exp = _detect_experience(text_lower)

    missing = []
    if not name:
        missing.append("applicant_name")
    if not email:
        missing.append("email")
    if track == TrackEnum.UNKNOWN:
        missing.append("track")

    is_complete = len(missing) == 0

    try:
        validated = InternshipApplication(
            applicant_name=name,
            email=email,
            track=track,
            skills=skills,
            availability=availability,
            years_of_experience=years_exp,
            is_complete=is_complete,
            missing_fields=missing,
        )
        return True, validated.model_dump(mode="json"), "Valid structured output."
    except ValidationError as exc:
        return False, {}, f"Schema validation failed: {exc.errors()}"


if __name__ == "__main__":
    model_cfg = os.getenv("MODEL_NAME", "gpt-4o-mini")
    sample = "Hi, I'm Amina Yusuf (amina.y@example.com), applying for software engineering with Python and FastAPI, full-time, 1 year experience."
    ok, data, msg = extract_application(sample, version="v2")
    print(f"Model config: {model_cfg} | Valid: {ok} | {msg}")
    print(data)
# Prompt Change Log, Risks, and Limitations

## Prompt Change Log
- **v1 (`SYSTEM_PROMPT_V1`)**: Basic extraction instruction with default null/unknown fallbacks.
  - *Observed Failure*: Weak boundary separation on adversarial text containing injection phrases and no explicit rule for `is_complete` or `missing_fields`.
- **v2 (`SYSTEM_PROMPT_V2`)**: Added strict grounding rules, prompt-injection isolation, allowed enum lists, explicit completeness rules, and two few-shot examples (complete vs. incomplete/ambiguous).
  - *Result*: Consistent schema conformance and explicit tracking of missing fields across normal, incomplete, ambiguous, malformed, and adversarial test cases.

## Remaining Risks & Limitations
1. **Keyword/Regex Heuristic Coverage**: Rule-based fallbacks can miss uncommon skill names, non-standard phrasing, or informal spellings.
2. **Name Extraction Edge Cases**: Regex name matching may miss single-word names or names preceded by unusual greetings.
3. **LLM API Variability**: When connected to a live LLM endpoint, outputs can still occasionally drift without strict structured-output/JSON-mode enforcement.
## Observed Failure Analysis (Run 1: 13/20 Passed)
- **Failed Cases (`TC01`, `TC02`, `TC03`, `TC04`, `TC17`, `TC18`, `TC20`)**: All 7 returned valid schema payloads (`actual_valid: True`) but set `actual_complete: False` despite containing name, email, and track information.
- **Root Cause**: Name extraction regex/casing in `_detect_name` missed certain name patterns or mixed-case segments after long/adversarial sentences, causing `applicant_name` to be `None` and marking `is_complete` as `False`.
- **Fix Applied**: Broadened `_detect_name` pattern matching for explicit name declarations (`i'm`, `i am`, `my name is`, `name is`) with proper title normalization and injection-phrase filtering.
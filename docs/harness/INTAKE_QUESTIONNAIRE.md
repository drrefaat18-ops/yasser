# Intake Questionnaire (approved by the user, DEC-027)

Claude asks these questions at the `intake` stage for every new book, one topic at a time. The answers go into `projects/<book>/brief.json`. No later stage runs until the brief, the generated rubric, the template, the theme and the agent overlays are approved (Standing Rule 7).

| ID | Topic | Ask about |
|---|---|---|
| A | Book identity | Title; author(s) and how they are credited; source files; whether the author has approved a rework |
| B | Domain | Main science and its sub-fields; which figure packs are needed (chemistry, charts, …) |
| C | Audience | Year of study; programmes or professions; what readers are assumed to already know |
| D | Perspectives | Whether the book uses professional perspective ("lens") boxes, and if so which perspectives |
| E | Goal | Evaluation only, or evaluation plus rework; if rework, the direction (simplify, broaden, update) |
| F | Language | Source language; output language; whether translation is needed; any required terminology |
| G | Size | Target length; number of chapters; limits on restructuring |
| H | Assessment | Whether MCQs are used, how many and in what format; cases or exercises |
| I | Context | Country; curriculum standards (e.g. NARS); the regulatory or professional framework |
| J | References | Citation style (Vancouver, APA, …); how recent references should be |
| K | Constraints | Content that must be kept; things that must not change; ISBN or publisher; deadline |
| L | Output | Word and/or PDF; page size; fonts; logo or branding; PDF engine (`word_com`, or `html` for the designed layout, DEC-043); palette and page (paper) colour; cover logos, institution line and eyebrow |
| M | Domain rubric pillars | Claude proposes the domain pillars and their weights; the user approves or edits them |

The exact field names in `brief.json` are defined by the STEP 1 spec (schema `brief`). They must cover A–M.

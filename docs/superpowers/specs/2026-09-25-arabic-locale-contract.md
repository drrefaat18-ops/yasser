---
type: interface-contract
step: 2
status: pending-codex-review (STEP 3)
date: 2026-09-25
core_spec: docs/superpowers/specs/2026-09-25-book-harness-core-design.md (approved at 0284376, DEC-031; amended in the STEP 2 commit as allowed by the ticket)
binding: docs/harness/VISION.md
---

# Arabic Locale — Interface Contract

This contract defines what the core must expose so an Arabic book can be ingested, checked, rendered and verified (DEC-006, DEC-019). It fixes **interfaces, data and acceptance criteria only**. Implementation is STEP 10.

Every field below maps to a named extension point of the core spec (§11 there): **EXT-LOC-1** locale profile, **EXT-LOC-2** direction and bidi, **EXT-LOC-3** labels bound to IDs, **EXT-LOC-4** reference policy, **EXT-LOC-5** acceptance corpus. The mapping table in §7 lists every field once.

Source of the requirements: Codex design review §5 (`docs/harness/codex-design-review-2026-09-25.md:243-287`, cited as *CDR §5*).

---

## 1. Principles

| # | Principle | Why |
|---|---|---|
| P1 | **Machine markers stay ASCII; display text is localized.** Learning-objective tags (`[LO1]`), question markers (`**Q1.**`), option letters (`A)`–`D)`) and answer keys (`**Q1. C**`) keep their ASCII form in the chapter Markdown. The renderer shows localized labels (`هدف ١`, `س١`, `أ`–`د`). | Parsing stays script-independent and identical for every language; key-balance and run checks work on the same letters. |
| P2 | **Headings and callouts are matched by the configured label for a stable ID** (core EXT-LOC-3). | No shared code compares against an English string. |
| P3 | **A text is processed with the profile of its own language.** The checker uses the output-language profile on chapters; ingest and translation checks use the source-language profile on source text. | A book can be Arabic in, English out, or the reverse. |
| P4 | **Protected spans are never localized:** DOIs, URLs, e-mail addresses, code, SMILES/SMARTS, chemical formulas, equations, units and gene or protein symbols keep Latin script and Western digits. | Converting them corrupts them. |
| P5 | **Numbers that are thresholds are calibrated, not copied** from English (CDR §5). | Arabic orthographic words carry clitics, so word counts differ from English for the same content. |

---

## 2. Locale profile `harness/locale/ar.json` (EXT-LOC-1)

The profile is data. Every locale-dependent function receives a profile object as a parameter; none reads a global language setting. A project may override any profile field through `template.locale_overrides` (core §4.3), which is covered by the intake approval.

| Field | Value for `ar` | Contract |
|---|---|---|
| `tag` | `ar` | matches `brief.language.*` values starting with `ar` |
| `script` | `Arab` | |
| `direction` | `rtl` | must equal `theme.direction` (core §4.6 rule 3) |
| `normalisation.compare` | `["NFC", "strip_tatweel", "strip_harakat", "unify_alef", "unify_ya"]` | applied before any **comparison** (glossary lookup, banned terms, termbase matching, discouraged verbs); never applied to text written to output |
| `normalisation.count` | `["NFC", "strip_tatweel"]` | applied before counting words |
| `tokenizer.kind` | `unicode-word` | a word is a maximal run of characters whose Unicode category is `L*`, `M*` or `N*`, plus `ZWNJ` (U+200C) and inner `'`, `’`, `-`, `.`, `/`, `%`, `٪` between word characters; stdlib `unicodedata` only (Rule 10) |
| `tokenizer.clitics` | `keep` | proclitics (`و`, `ف`, `ب`, `ل`, `ك`, `ال`) are not split; counts are orthographic words |
| `sentence_terminators` | `[".", "!", "?", "؟", "…"]` | a sentence ends after a run of terminators followed by whitespace or end of line; `؛` (Arabic semicolon) and `،` (Arabic comma) never end a sentence |
| `sentence_exceptions.abbreviations` | `["د.", "أ.", "أ.د.", "م.", "ص.", "ت.", "e.g.", "i.e.", "et al.", "vs.", "Fig."]` | a terminator inside a listed abbreviation does not end a sentence |
| `sentence_exceptions.decimals` | `true` | `.` or `٫` (U+066B) between two digits of the same system is a decimal separator, not a terminator |
| `digits.accepted` | `["western", "arabic-indic"]` | parsing of chapter numbers, citation numbers, reference numbers and figure numbers accepts both systems (`0-9`, `٠-٩` U+0660–U+0669) |
| `digits.output` | `arabic-indic` | the digit system the renderer uses for page numbers, chapter and figure numbers and list numbering; a project sets `western` via `template.locale_overrides.digits.output` (asked under questionnaire F) |
| `digits.mixed_number` | `fail` | a single number mixing both systems is an error (`AR-DIGIT-MIXED`) |
| `digits.body_consistency` | `warn-as-check` | body numbers outside protected spans that use the non-configured system produce `AR-DIGIT-INCONSISTENT` |
| `list_separators` | `[",", "،"]` | accepted inside citation groups, e.g. `[1، 3]` |
| `range_separators` | `["-", "–"]` | accepted inside citation groups |
| `percent_signs` | `["%", "٪"]` | both accepted |
| `ordinal_words` | map of `الأول`…`الثلاثون` → 1…30 (masculine and feminine forms) | lets `chapter_heading_pattern` accept `الفصل الثالث` as chapter 3 |
| `chapter_heading_pattern` | `^# الفصل (?P<num>[0-9٠-٩]+\|<ordinal>)\s*[:：]\s*(?P<title>.+)$` | `<ordinal>` expands from `ordinal_words` |
| `figure_caption_pattern` | `شكل ({chapter}-{n})` | numbers rendered in `digits.output` |
| `table_caption_pattern` | `جدول ({chapter}-{n})` | |
| `discouraged_objective_verbs` | normalised patterns for "understand / know / be aware of": `[يت]?فهم`, `فهم`, `[يت]?عرف`, `معرفة`, `[يت]?درك`, `إدراك`, `[يت]?لم ب`, `الإلمام` | matched on the normalised objective line at word boundaries |
| `banned_terms` | `[{pattern: "(ال)?سيد[- –](ال)?عبد", replacement: "القائد–التابع"}]` | merged with `template.banned_terms` |
| `readability` | `{mean_sentence_max, long_sentence_words, long_share_max, status: "calibrated", provenance}` | values are **computed in STEP 10** by the rule in §2.1; the profile never ships with uncalibrated values |
| `default_labels` | §4 | used when the template or theme does not set a label |
| `quote_marks` | `["«", "»"]` | accepted around quotations; not counted as words |

### 2.1 Readability calibration rule

1. Corpus: ≥ 500 aligned English–Arabic sentence pairs of **human-authored** parallel text with its licence recorded, stored at `tests/fixtures/locale/ar/parallel/` (a sample of the UN Parallel Corpus or an equivalent openly licensed source; provenance in `SOURCE.md` there).
2. Compute `r` = median over pairs of (Arabic word count ÷ English word count), both counted with their own profiles.
3. `ar.mean_sentence_max = round(en.mean_sentence_max × r)`; `ar.long_sentence_words = round(en.long_sentence_words × r)`; `ar.long_share_max = en.long_share_max`.
4. `provenance` records the corpus, `r`, the English values used and the date.

A project may still set its own values through `template.readability` at intake.

---

## 3. Direction and bidi contract for DOCX (EXT-LOC-2)

The core renderer creates every paragraph, run, table and section through **one** function that applies direction and language from the theme (core EXT-LOC-2). For `theme.direction = "rtl"` it must emit the following. Each row is an acceptance assertion checked on the built DOCX XML (§6.2).

| Element | Required OOXML | Notes |
|---|---|---|
| document defaults (`styles.xml` `w:docDefaults/w:rPrDefault`) | `w:lang w:val="en-US" w:bidi="<theme.lang_tag>"`; `w:rFonts w:cs="<theme.fonts.complex_script>"` | `lang_tag` default `ar-EG` (CDR §5); any tag starting `ar-` is valid |
| settings (`settings.xml`) | `w:themeFontLang w:bidi="<theme.lang_tag>"` | |
| every paragraph style and paragraph in the body | `w:pPr/w:bidi` | |
| paragraph alignment | theme values `start`, `end`, `center`, `both` mapped to OOXML so that `start` renders at the **right** margin | the mapping is proven by the rendered evidence pages (§6.3), not assumed |
| every run of Arabic text | `w:rPr/w:rtl`; `w:rFonts w:cs`; `w:szCs` equal to `w:sz`; `w:bCs`/`w:iCs` whenever `w:b`/`w:i` | |
| runs of Latin text or protected spans inside an Arabic paragraph | no `w:rtl`; `w:lang w:val="en-US"`; Latin fonts in `w:ascii`/`w:hAnsi` | the renderer splits text into runs by strong bidi class (`unicodedata.bidirectional`: `R`/`AL` → RTL run, `L` → LTR run; neutrals and digits join the preceding run; a leading neutral joins the following run) |
| protected span boundaries | a Left-to-Right Mark (U+200E) on each side of an LTR run whose neighbour character is neutral | keeps DOIs, URLs, formulas and parentheses in order |
| tables | `w:tblPr/w:bidiVisual`; the first logical column renders at the right; cell margins mirrored | |
| sections | `w:sectPr/w:bidi`; `w:pgNumType w:fmt="hindiNumbers"` when `digits.output = arabic-indic`, else `decimal` | page numbers and TOC page numbers follow this format |
| lists (bullets and numbers) | numbering levels with indent and hanging indent on the **reading-start** side; `w:numFmt` `hindiNumbers` or `decimal` per `digits.output` | proven by the list evidence page |
| headers and footers | bidi paragraphs; running head book title at reading start, chapter title at reading end | mirror of the LTR layout |
| captions | `figure_caption_pattern` / `table_caption_pattern` from the profile, digits per policy | |
| TOC | TOC field with TOC1/TOC2 styles carrying `w:bidi`; heading text `theme.labels.contents` | Word fills it via COM, as today (`rework/tools/build_book.py:945-947`) |
| equations (OMML) | kept LTR (`m:oMathPara` without bidi) | formulas read left to right in Arabic textbooks |
| core properties | `dc:language` = `theme.lang_tag` | |
| fonts | preset `rtl-textbook`: body `complex_script` = **Sakkal Majalla**, headings and UI `complex_script` = **Segoe UI**; Latin fonts as `ltr-textbook` | both ship with stock Windows (present on this machine in `C:\Windows\Fonts`: `majalla.ttf`, `majallab.ttf`, `segoeui.ttf`); preflight checks them |

**Theme fields used:** `direction`, `lang_tag`, `fonts.complex_script`, `alignment.*`, `lists.*`, `labels.*`, `preset` (core §4.4). The preset file `harness/presets/rtl-textbook.json` is created in STEP 10.

### 3.1 RTL rules for lists, tables and the TOC (summary)

| Structure | Rule | Evidence page |
|---|---|---|
| lists | marker at the right; hanging indent opens to the left; nested levels step leftwards; numbers per `digits.output` | list page |
| tables | first column at the right; header row repeated; text in cells right-aligned; numeric columns keep digits per policy | table page |
| TOC | entries right-aligned, page numbers at the left end with a dot leader, levels indented leftwards, page numbers per `digits.output` | TOC page |

---

## 4. Labels bound to stable IDs (EXT-LOC-3)

Default Arabic labels in `ar.json` → `default_labels`, keyed by the IDs the core already uses. A project's `template` and `theme` may replace any of them.

| ID (core field) | Default Arabic label |
|---|---|
| `theme.labels.contents` | المحتويات |
| `theme.labels.update_toc_instruction` | انقر بزر الفأرة الأيمن واختر «تحديث الحقل» لإنشاء المحتويات. |
| `theme.labels.chapter` | الفصل |
| `theme.labels.part` | الجزء |
| `theme.labels.glossary` | مسرد المصطلحات |
| `theme.labels.figure` | شكل |
| `theme.labels.table` | جدول |
| `theme.labels.question_prefix` | س |
| `theme.labels.objective_prefix` | هدف |
| section role `opening` | حالة افتتاحية |
| section role `objectives` | أهداف التعلم |
| section role `takeaways` | النقاط الرئيسية |
| section role `assessment` | التقييم الذاتي |
| section role `answers` | الإجابات والتعليلات |
| section role `references` | المراجع |
| section role `how_to_use` | كيف تستخدم هذا الكتاب |
| `template.assessment.case_question.label` | سؤال الحالة |
| `template.assessment.mcq.option_display_labels` | `["أ", "ب", "ج", "د"]` (abjad order; extends `ه`, `و` if a book has more options) |

Callout labels are always project data (core `template.callouts[].label`); the profile supplies none.

**Glossary term form:** a bold Arabic term may carry a Latin gloss in parentheses right after it, e.g. `**التعلم الآلي** (machine learning)`. The checker captures the gloss as `gloss` in its parsed representation; lookup uses the normalised Arabic term. The glossary file uses the same form. The gloss is what the translation termbase links to (translation contract §3).

---

## 5. Arabic reference policy (EXT-LOC-4)

### 5.1 Two separate results per reference

`verify_refs` reports each numbered reference with two fields (core EXT-LOC-4):

| Field | Values |
|---|---|
| `doi_status` | `exists`, `not_found`, `error`, `no_doi` |
| `title_status` | `match`, `mismatch`, `manual_pending`, `manual_ok`, `not_applicable` (no DOI) |

A DOI that exists but whose title cannot be compared automatically is `manual_pending`, never `match`.

### 5.2 Title-match modes (`template.references.title_match.mode`)

| Mode | Behaviour |
|---|---|
| `heuristic` | tokenise the reference line and the registry title with the profile of each text's script (Arabic tokens via `ar`, Latin via `en`), apply `normalisation.compare`, take the first `words` content tokens of the registry title (default 6, tokens of ≥ 3 characters), match if the share present in the line ≥ `threshold` (default 0.6). Compare against every registry title field returned (`title`, `original-title`, `short-title`); any match counts. |
| `original-language` | the reference line carries the original title inside the marker `template.references.original_title_marker` (default for `ar`: `[العنوان الأصلي: …]`; default for `en`: `[Original title: …]`); matching uses the text inside the marker only, with the heuristic rule. A line with no marker is `manual_pending`. |
| `manual` | every DOI reference is `manual_pending` until resolved. |

### 5.3 Manual verification record

`projects/<p>/references-manual.json` (schema `references-manual.v1`): entries `{chapter_id, n, doi, verified_title, evidence_url, verified_on, dec_id}`. A matching entry turns `manual_pending` into `manual_ok`. The `dec_id` names the `decisions.md` row where the user or Claude recorded the check.

### 5.4 Pass rules

| Outcome | Checker ID | Blocks `complete rework`? |
|---|---|---|
| `not_found` | `REF-NOT-FOUND` | yes |
| `error` | `REF-ERROR` | yes |
| `mismatch` | `REF-TITLE-MISMATCH` | yes |
| `manual_pending` | `REF-MANUAL-PENDING` | yes |
| `no_doi` not allowed by `template.references.no_doi_policy` | `REF-NO-DOI-DISALLOWED` | yes |
| `exists` + `match` or `manual_ok`; allowed `no_doi` | — | no |

Citation numbers inside the text and the reference list numbering accept both digit systems; DOIs and URLs are protected spans (P4) and never converted.

---

## 6. Acceptance corpus (EXT-LOC-5)

Stored under `tests/fixtures/locale/ar/`, discovered by directory by the test runner. Each case file holds input and literal expected output.

### 6.1 Text-processing cases

| Directory | Cases (minimum) | Literal expectation |
|---|---|---|
| `tokenize/` | harakat, tatweel, proclitics, Latin terms inside Arabic, both digit systems, `٫` decimals, `٪`, hyphenated compounds | exact word count per case |
| `sentences/` | `؟`, `…`, `!؟`, abbreviations from §2, decimals in both systems, URLs, `؛` and `،` inside sentences | exact sentence list per case |
| `digits/` | pure Western, pure Arabic-Indic, mixed-in-one-number, numbers inside protected spans | `AR-DIGIT-MIXED` / `AR-DIGIT-INCONSISTENT` present or absent as stated |
| `labels/` | one Arabic chapter using Arabic section, callout and perspective labels, ASCII markers, Arabic ordinal chapter heading | checker report with zero failing checks; parsed section IDs listed literally |
| `objectives/` | objective lines with each discouraged verb form, and a clean line | `LO-VERB` present exactly for the listed lines |
| `glossary/` | bold term with and without Latin gloss; term with harakat vs glossary entry without | lookup succeeds after normalisation; gloss captured |
| `references/` | Arabic registry title (mocked), English reference in an Arabic book, translated title with original-title marker, marker missing, manual record present | the `doi_status` / `title_status` pair per reference |
| `parallel/` | ≥ 500 aligned pairs with `SOURCE.md` (licence, provenance) | calibration output of §2.1 is reproducible to the stored values |

### 6.2 DOCX XML assertions

`tests/fixtures/locale/ar/docx/assertions.json`: a list of `{xpath, expect}` checked against the DOCX built from the `labels/` fixture book. It contains at least one assertion for each row of the §3 table (docDefaults `w:bidi` language, `w:themeFontLang`, `w:bidi` on body paragraphs, `w:rtl` on Arabic runs and its absence on Latin runs, `w:szCs`, `w:rFonts/@w:cs`, `w:bCs`, `w:bidiVisual` on tables, `w:sectPr/w:bidi`, `w:pgNumType/@w:fmt`, list `w:numFmt`, TOC field present, `dc:language`).

### 6.3 Rendered evidence (STEP 10 exit)

PDF pages rendered from the fixture book and saved under `docs/harness/reviews/step10-evidence/`: a **TOC page**, a **table page**, a **list page** and a **mixed-script page** (Arabic paragraph containing an English term, a DOI, a URL, a formula, a percentage and a parenthesised citation). Codex inspects them in its STEP 10 review.

### 6.4 Arabic check IDs added to the core catalogue

`AR-DIGIT-MIXED`, `AR-DIGIT-INCONSISTENT`, `REF-MANUAL-PENDING`. All other checks keep their core IDs (core §9.3) and run unchanged on Arabic text through the profile.

---

## 7. Field → extension point map

| Contract field | Core extension point |
|---|---|
| `tag`, `script`, `direction` | EXT-LOC-1 (profile); `direction` also EXT-LOC-2 |
| `normalisation.compare`, `normalisation.count` | EXT-LOC-1 |
| `tokenizer.kind`, `tokenizer.clitics` | EXT-LOC-1 |
| `sentence_terminators`, `sentence_exceptions.*` | EXT-LOC-1 |
| `digits.accepted`, `digits.output`, `digits.mixed_number`, `digits.body_consistency` | EXT-LOC-1 (via `template.locale_overrides` for `output`) |
| `list_separators`, `range_separators`, `percent_signs`, `quote_marks` | EXT-LOC-1 |
| `ordinal_words`, `chapter_heading_pattern` | EXT-LOC-1 |
| `figure_caption_pattern`, `table_caption_pattern` | EXT-LOC-1 |
| `discouraged_objective_verbs`, `banned_terms` | EXT-LOC-1 |
| `readability.*` and the calibration rule | EXT-LOC-1; corpus in EXT-LOC-5 |
| `default_labels` (all of §4) | EXT-LOC-3 |
| `template.assessment.mcq.option_display_labels`, `theme.labels.question_prefix`, `theme.labels.objective_prefix`, `theme.labels.table` | EXT-LOC-3 |
| glossary `gloss` in the parsed representation | EXT-LOC-3 (and EXT-TR-3 for termbase linking) |
| all §3 OOXML obligations, `theme.lang_tag`, `theme.fonts.complex_script`, preset `rtl-textbook` | EXT-LOC-2 |
| `doi_status`, `title_status` | EXT-LOC-4 |
| `title_match.mode`, `original_title_marker`, `references-manual.json` | EXT-LOC-4 |
| every §6 directory, DOCX assertions, rendered evidence | EXT-LOC-5 |

---

## 8. Out of scope for this contract

Internals of the tokenizer, splitter, run-splitting algorithm and renderer (STEP 10); the translation stage (translation contract); any language other than Arabic and English.

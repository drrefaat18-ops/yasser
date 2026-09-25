# STEP 3 — Fix Protocol record (DEC-030)

Review: `docs/harness/reviews/step3-review.md` (Codex, read-only, reviewed commit `445dc0d`, verdict `fail`, 15 blocker/major, 2 minor). This was the one review of these specs; there is no second round.

**Dispatch note.** The first dispatch (run `yasser-2026-09-25T15-54-44-094Z`) produced no review. Every shell read was refused with "blocked by policy", so Codex inspected no files. Root cause: the `--ignore-user-config` flag skipped the user Codex config, and that config holds the Windows sandbox read permissions. Earlier successful runs used `ignoreUserConfig: false`. It was re-dispatched without the flag (run `yasser-2026-09-25T15-56-20-502Z`, `touchedFiles: []`). This does not count as a second review, because the first run reviewed nothing.

**Verification script:** `verify_step3.py` (session scratchpad; its full text is reproduced at the end of this file). It checks:
- every backticked inventory target key against the declared fields of the owning §4/§11 section, with wildcards banned;
- that the replaced phrases are gone;
- that there are no Markdown-escaped pipes and no TBD/TODO;
- that every EXT ID used is defined;
- that every new check ID is mapped and tested.

Result: `inventory keys checked: 132`, `ALL CHECKS PASS`, exit 0.

Mutation proof: injecting `theme.page.gutter_bogus` and `theme.fonts.*` into INV-29 made it exit 1 with both errors named.

| ID | Real / rejected | Root cause | Siblings found (same class) | Fix | Verification → result |
|---|---|---|---|---|---|
| S3-01 | Real. The graph showed `translate` as a peer of the six vision phases, with no mapping to them. | The spec treated "stage" (receipt unit) and "phase" (vision step) as the same thing and never mapped one onto the other. | `new` and `intake` are also not among the six phases, and were unmapped too. | Core §2.1: a phase-map table. `new`/`intake` are the pre-work gate, and `translate` + `rework` together form phase 4 (Rewrite), with order unchanged. Translation contract §2 and EXT-TR-1 say the same. The stage id is kept because the ticket (STEP 2, STEP 11) names a translation stage. | `grep -n "Vision phase" core` → table present; `grep -c "first step of vision phase 4" tr core` → 1 each |
| S3-02 | Real | Staleness was defined from the ticket's minimum (inputs only), so outputs were recorded but never re-checked. The audit flow then relied on editing another stage's outputs. | (a) Design edited `template.json`/`theme.json`, which are intake outputs (§3). (b) Rework edited the translate-owned trace map and additions file (= S3-06). | §2.3: outputs are re-hashed, and a missing file is stale. There is a one-owner-per-file rule. The audit fix loop is now `abort audit` → `begin/complete rework` → `run build` → `begin/complete audit`. The design-time template change uses a new `begin intake --amend` path (§3). | Verifier stale-phrase list; `grep -n "output hash" core` → §2.3 rule present |
| S3-03 | Real | Receipts hash "every output", but the receipt lives inside `state.json`, and `new` had a non-file input. | `decisions.md` and `state.lock` have the same self-reference problem. | §2.3 defines control-plane files (`state.json`, `state.lock`, `decisions.md`), which are never hashed in receipts. A new receipt field `args`. The `new` row lists `args: {slug}` and no `state.json` output. `decisions.md` is bound through the row hashes instead (S3-16). | `grep -n "Control-plane files" core` → present; `slug argument` gone (verifier) |
| S3-04 | Real | The spec copied the ticket's "approvals that exist" wording for `verify`, and wrote gates per row rather than as one derived rule. | `complete` did not re-check gates, so an approval that went stale mid-stage could still complete. | §2.3 `require_gates`: one function called by `begin`, `run`, `complete`, `verify` and legacy tools. It derives the required approvals from `STAGES`, and a missing approval fails. §2.2 preamble: rows list only stage-specific conditions. | `each approval that exists` gone (verifier); `grep -n require_gates core tr` → core §2.2/§2.3, translation §2 |
| S3-05 | Real | Only the file write had a lock; nothing represented "a stage is in progress". | Agentic `complete` could be called for a stage that was never begun, or begun by another session. | §2.3: an `active_run` lease with a nonce, one per project. `complete --nonce`. `abort <stage> --reason` is the only recovery and is logged in `aborts[]`. | `grep -n "active_run\|abort" core` → §2.3, §2.2 audit row, §3 |
| S3-06 | Real | Two stages wrote the same files: the trace map and the additions file. | This is the same class as S3-02(a). The rejected-term check was also missing. | The translate-owned `trace/translation-map.json` (`kind: translation`) is separate from the rework-owned `trace/source-target-map.json` (`kind: final`), each with its required and forbidden fields. Proposals go to `terms/translate-proposals.json` and `terms/rework-proposals.json`, with ID prefixes that cannot collide. `termbase-additions.json` is now a resolution record written only by `terms resolve --dec`. New checks `TB-REJECTED-PRESENT` and `TB-PROPOSAL-OPEN`, both in acceptance criterion 1. | Verifier: `translation half`, `status: proposed`, `appended by` gone; both new IDs mapped and tested |
| S3-07 | Real | Audit inputs were listed for the untranslated case only. | Audit also rescores G1 against the source, yet `brief.json` and `ingest/normalized.md` were missing from its inputs even without translation. | Core §2.2: audit inputs gain `brief.json` and `ingest/normalized.md`, plus the translation evidence conditionally. `codex_audited_build` becomes `codex_audited_inputs`. Translation §6 lists the bound artifacts. | `codex_audited_build` gone (verifier) |
| S3-08 | Real | The brief used BCP-47 tags, but profiles, pair logic and cross-rules compared whole tags. | Cross-rule 3 (`theme.lang_tag` vs output) had the same whole-tag comparison, and Arabic §3 said "any tag starting `ar-`". | The primary subtag selects the profile and decides translation. The full tag is used only for `theme.lang_tag` / Word language. Updated core §4.1, §4.6 rules 2–3, EXT-LOC-1, Arabic `tag` row and §3 docDefaults, translation §1. New acceptance criterion 6 (`ar-EG→en-GB`, `en-GB→en-US`, `fr→ar`). | Verifier: `language.source ≠ language.output` and `starting with \`ar\`` gone |
| S3-09 | Partly real. The regex is correct once the Markdown table renders `\|` as `|`, but the raw file is ambiguous, and `<ordinal>` expansion (escaping, order, feminine and two-word forms) was undefined. | A regex was placed in a Markdown table cell, and a pattern template was specified without its expansion rule. | A grep for `\|` in all three specs found only this one. | The regex moves to a code block in the new Arabic §2.2, with a defined expansion: `re.escape`, longest first, masculine and feminine forms, matched after normalisation, and `num` converted to an integer. The `labels/` corpus gains Western, Arabic-Indic, masculine, feminine and two-word ordinal headings. | Verifier: no `\|` in any spec |
| S3-10 | Real | The theme had a single complex-script font slot, and the equation rule described OMML in isolation, ignoring the containing paragraph. | The "every paragraph gets `w:bidi`" row contradicted any LTR equation paragraph. | New `theme.fonts.complex_script_heading` (core §4.4, EXT-LOC-2; Arabic §3 heading-style row and fonts row). Display equations get their own paragraph with no `w:bidi` and centred alignment; inline math is handled as an LTR run with LRM. The bidi row carves out equation paragraphs. §6.2/§6.3 assert both. | `grep -n complex_script_heading core ar` → core §4.4 + EXT-LOC-2, Arabic §3, §7 |
| S3-11 | Real | The G1 "owns" text and overlap rule 2 were written separately, and both claimed claim-support. | The G4 "owns" text omitted the case of a claim that needs a citation and has none. | G1 owns falsity and claim-support mismatch. G4 owns existence, metadata, currency, hierarchy and missing citations. The ownership table and overlap rules 1–2 now use the same wording. | `grep -n "claim-support\|does not support" core` → G1 row and rule 1 only |
| S3-12 | Real | The weight bounds (5–25) were chosen without checking them against the pillar count (1) and the fixed sum (40). The caps were prose. | A scorecard could claim a cap without evidence. | Each domain pillar is now worth 5–40 (1–4 pillars, sum 40). `hard_caps[].trigger {severity, min_count, tag}` is evaluated against findings and fixes. `findings.tags[]`; `scorecard.caps_applied[]`. `complete` fails when a cap is missing, spurious or exceeded. | Verifier: `from 5 to 25`, `{condition, max_score}` gone |
| S3-13 | Real | The inventory used wildcard targets (`.*`) to cover several hardcoded facts, so nothing forced each fact onto a declared field. | Duplicate keys: `template.errata.file` vs `template.paths.errata`. `defaults.json` had no declared fields. `build/` output location was implicit. | 19 rows rewritten with exact keys. Non-configurable sub-parts are named as harness constants (Q/LO marker grammar), preset constants (`title_page_layout`), fixed behaviour (hidden Word instance) or the fixed `build/` directory. `template.ingest` gains `toc_start_pattern` and `toc_entry_pattern`. `errata.file` removed. `defaults.json` fields declared in §4.5. The completeness line states the mechanical rule. | Verifier: 132 keys checked, 0 undeclared, 0 wildcards; the mutation test fails as expected |
| S3-14 | Real | Project selection was designed for production only, and fixture use was not traced through it. | Translation acceptance criterion 4 made the same assumption. | New core §9.6: a temporary `git init` repository with a copy of `harness/` (committed, so `tool_sha` works) and the fixture copied into `projects/`. The real CLI runs there. No bypass flag. Referenced from §1, §3 and translation §9. | `grep -n "9.6" core tr` → §1, §3, §9.6, translation §9 |
| S3-15 | Real | The text-fidelity denominator ignored an omission that the template itself authorises. | No other authorised omission exists (INV-05/07 cleanups are `removed`, not omissions). | §2.4: a configured-omission rule (only the source TOC today, bounded by `toc_start_pattern`/`toc_end_pattern`). `omitted[]` is recorded and reported, and the denominator is source − omitted. | `grep -n "Configured omissions" core` → §2.4 |
| S3-16 | Real (minor) | The approval stored a DEC reference but not the content of the DEC row. | `references-manual.json` entries and term resolutions also cite a DEC by ID only. `references-manual.json` was also missing from the rework inputs. | `dec_row_sha256` is stored and re-checked by `require_gates`. It is also added to term resolutions and references-manual entries. `references-manual.json` becomes a hashed rework input. | `grep -c dec_row_sha256 core ar tr` → 1+ each |
| S3-17 | Real (minor) | The chemistry IDs were listed without their stage effect, unlike the `FIG-*` IDs. | none | Core §7.5 effect table: invalid, sanitise and mismatch fail build. `CHEM-UNVERIFIED` is reported, and `complete audit` refuses until a live pass or a `ruled by user` row with a DEC. It is never reported as pass. | `grep -n "CHEM-UNVERIFIED" core` → §7.5 table |

**Closing checks run after all fixes:**
- `python verify_step3.py` → exit 0.
- The mutation run → exit 1 with both errors named.
- The STEP 1/2 exits still hold: 48 INV rows with source columns untouched (the rewrite changed only the Target cell), A–M rows unchanged, the TBD grep empty, and the EXT IDs used ⊆ the IDs defined.

**Scope note for the user.** Two fixes go beyond Codex's wording and are part of the approval:
- `begin intake --amend` (S3-02 sibling).
- Translation kept as a stage id, mapped into phase 4, rather than folded into `rework` as Codex proposed. The ticket names a translation stage, and the vision fixes phases, not receipt units.

## Appendix: `verify_step3.py`

```python
"""STEP 3 verification: inventory keys declared, stale phrases gone, EXT IDs consistent."""
import re, sys
D = 'docs/superpowers/specs/'
core = open(D + '2026-09-25-book-harness-core-design.md', encoding='utf-8').read()
ar = open(D + '2026-09-25-arabic-locale-contract.md', encoding='utf-8').read()
tr = open(D + '2026-09-25-translation-contract.md', encoding='utf-8').read()
fail = []

def section(start, end):
    return core[core.index(start):core.index(end)]

owners = {
    'template': section('### 4.3', '### 4.4'),
    'theme': section('### 4.4', '### 4.5'),
    'brief': section('### 4.1', '### 4.2'),
    'chapter-plan': section('### 4.5', '### 4.6'),
    'defaults': section('### 4.5', '### 4.6'),
    'locale': section('| EXT-LOC-1', '| EXT-LOC-2'),
}
inv = section('## 10.', '## 11.')
rows = [l for l in inv.splitlines() if l.startswith('| INV-')]
assert len(rows) == 48, len(rows)
checked = 0
for row in rows:
    target = row.split('|')[4]
    for key in re.findall(r'`([a-z-]+(?:\.[A-Za-z_<>\[\]*-]+)+)`', target):
        prefix, *parts = key.split('.')
        if prefix not in owners:
            continue
        checked += 1
        if '*' in key:
            fail.append(f'wildcard {key} in {row[:10]}')
        text = owners[prefix]
        for part in parts:
            name = part.replace('[]', '')
            if name.startswith('<'):
                continue
            if not re.search(r'(?<![A-Za-z_])' + re.escape(name) + r'(?![A-Za-z_])', text):
                fail.append(f'{row[2:8]}: {key} -> "{name}" not declared in {prefix} section')
print('inventory keys checked:', checked)

stale = {
    'codex_audited_build': core + tr,
    'each approval that exists': core,
    'from 5 to 25': core,
    '{condition, max_score}': core,
    'slug argument': core,
    'translation half': tr,
    'status: proposed': tr,
    'appended by `translate` and `rework`': tr,
    'starting with `ar`': ar,
    'language.source ≠ language.output': core + tr,
    '`file`, `status_column`': core,
}
for phrase, text in stale.items():
    if phrase in text:
        fail.append(f'stale phrase still present: {phrase}')
for name, text in (('core', core), ('ar', ar), ('tr', tr)):
    if '\\|' in text:
        fail.append(f'markdown-escaped pipe in {name}')
    if re.search(r'\b(TBD|TODO)\b', text):
        fail.append(f'TBD/TODO in {name}')

defined = set(re.findall(r'^\| (EXT-[A-Z]+-\d) ', core, re.M))
used = set(re.findall(r'EXT-[A-Z]+-\d', ar + tr))
if used - defined:
    fail.append(f'undefined EXT ids: {used - defined}')

for cid in ('TB-REJECTED-PRESENT', 'TB-PROPOSAL-OPEN', 'TR-PAIR-UNSUPPORTED'):
    if tr.count(cid) < 2:
        fail.append(f'{cid} defined but not tested/mapped')

print('\n'.join(fail) if fail else 'ALL CHECKS PASS')
sys.exit(1 if fail else 0)
```

# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Markdown chapter sources in `rework/` → python-docx builds a Word file → Microsoft Word (COM) updates the contents page and exports the PDF. Word and PDF come from one source, so they always match.

## Users

Year 1–2 (pre-clinical) students of medicine, pharmacy, physical therapy and the health sciences, taking one shared course. They read the book on laptops and phones, and sometimes print chapters at home. Teaching staff edit the Word file.

## Product Purpose

*Artificial Intelligence in Health Care: An Interprofessional Introduction* is a university textbook. It teaches what AI is, how to judge an AI claim, and how AI touches each of the four professions. Success means a student can read it end to end, find any chapter, box or reference in seconds, and use the MCQs to test themselves.

## Positioning

It is one book for four professions. Every chapter has "Through Four Lenses" boxes and running patient cases (Amal, Karim and Lina) that cross professional lines.

## Operating Context

- Distributed as an A4 PDF for reading on screen and printing at home.
- Also distributed as an editable .docx for the department.
- Links in the contents page and to references should work in the PDF.

## Capabilities and Constraints

- Page size: A4.
- Fonts must be installed on stock Windows so the .docx opens correctly on department machines.
- There is no ISBN, publisher or copyright registration. Never invent these.

## Brand Commitments

- The book should look like a conventional university textbook, played straight. The user asked for "كتاب جامعة" (a university book).
- Author credit is "Assistant Prof. Dr. Shereen Elsaid Elkholy" as sole author, until she confirms otherwise.

## Evidence on Hand

- Chapter sources: `rework/ch01…ch11`, `00-front-matter.md` and `glossary.md`.
- Figures: `rework/figures/` and `images/`.
- Review report: `rework/REVIEW_REPORT.md`.
- The patient cases are fictional.

## Product Principles

1. Wayfinding first. Readers should always be able to see the chapter, section and page they are on.
2. Each box type gets one consistent look, so readers learn to recognise it.
3. Word and PDF come from one source. Nothing is hand-edited in only one of them.

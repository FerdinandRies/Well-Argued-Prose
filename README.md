# JournalProse

**Advanced Scholarly Writing Standards**

*Most writing tools check your sentences. Peer review judges your arguments.*

JournalProse is an argument-first framework for precise academic English and
natural scholarly prose. Its 50 public rules are organized in eight levels that
run from manuscript integrity to final review, and every language rule operates
under a standing constraint: **revision at the sentence level stays answerable
to the governing claim and the reasoning chain.** When a sentence exposes a
logical problem, the framework sends the issue upward to the argument. Where a
sentence and the argument conflict, the argument governs.

## Why JournalProse is different

- **Argument before style.** The level structure (L0–L7) fixes the base text,
  the governing claim, and the inference chain before any sentence is polished.
  Style rules operate inside limits the argument sets: quantifiers, modals,
  conditions, and conclusions stay fixed unless the author revises the argument
  itself.
- **Compression that protects the argument.** Shortening is restricted to real
  redundancy. Argument chains, concept criteria, test cases, objection replies,
  and literature reconstructions are protected objects, and every compression
  round ends with a preservation check.
- **Citation discipline.** Each source carries one argumentative function. The
  checks flag semicolon-stacked citations and mechanical author-by-author
  queuing, and a fifth independent source in one argumentative paragraph
  prompts the reviewer to redistribute sources across the discussion.
- **Evidence as the review record.** A human review checklist records textual
  evidence, open problems, and unresolved items, so a completed review shows
  what was checked, what was found, and what remains open. The scholarly
  judgment stays with the reviewer.

## Inside the release

| Component | Count |
|---|---|
| Core writing rules (JP2-001 – JP2-050) | 50 |
| Logical levels (L0–L7) | 8 |
| Task workflows | 6 |
| Automated surface checks | 21 |
| Human review dimensions | 10 |
| Tests passing | 130 |

The levels form one dependency chain:

```text
Manuscript Integrity · L0
  → Argument Architecture · L1–L2
  → Paragraph and Sentence Construction · L3–L4
  → Scholarly Voice and Literature · L5–L6
  → Revision Integrity and Final Review · L7
```

## Six workflows

1. **Manuscript Revision** — 46 rules across structure, concepts, inference,
   paragraphs, and sentences.
2. **Language and Style** — 29 rules for grammar, reference, terminology, and
   natural scholarly expression.
3. **Foundational Argument Review** — 17 rules for conditions, quantifiers,
   modality, causation, evidence, and fact-to-value bridges.
4. **Literature and Citation Review** — 11 rules against citation stacking,
   density drift, and author queuing.
5. **Argument-Preserving Compression** — 10 rules that shorten text while
   protecting premises, counterexamples, qualifications, and source analysis.
6. **Final Review** — 33 rules plus the 10-dimension human checklist before
   submission.

## What the tool does today

The command-line tool runs locally. It locates candidate problems with line and
column positions: formulaic negative-contrast constructions, template phrases,
promotional wording, vague reference, stacked hedges, semicolon citation
clusters, and citation density. It reads Markdown, plain text, and — with the
optional dependency — Word documents. Manuscripts stay on the author's
machine, and every automated finding is a located candidate for review, ready
to hand to the author or to an AI assistant working under the same rules. The
six workflows organize the full rule set into guided review, with findings
recorded as textual evidence, item by item.

## Where JournalProse is going

Version 0.2.0 is the foundation layer of a larger standards system, and its
architecture already defines the growth path:

- **Deeper execution of the existing rules** — fuller grammar diagnosis and
  context-sensitive reference resolution, growing the current surface checks
  toward the full standards the handbook states.
- **Semantic preservation checks** — comparing a manuscript before and after
  revision and reporting what changed in its claims, qualifications, and
  citation functions.
- **Rule-driven, traceable editing** — automated suggestions that name the
  rule, the evidence in the text, and the repair, so an author can accept,
  reject, or audit every change.

The foundation is public and stable by design: future capabilities extend
these 50 rules.

## Who it is for

Researchers preparing manuscripts for serious peer-reviewed journals who want
each revision decision traceable to an explicit, inspectable standard.

## Getting started

```bash
python -m pip install .
journalprose show JP2-033
journalprose guide compression
journalprose audit examples/sample-manuscript.md
```

**Maintainer:** FerdinandRies. **Code:** MIT. **Rules, documentation, and
original examples:** CC BY 4.0. Version 0.2.0.

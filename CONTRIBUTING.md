# Contributing

We welcome substantive corrections, concrete examples, and improvements to the software.

For **rule changes**, identify the current rule, the precise reasoning or prose failure it does not catch, a worked example, and the proposed improvement. A related publication is useful evidence, not a reason by itself to overwrite a rule. Keep numbered rules stable; propose new numbers only with a rationale.

For **code changes**, add a minimal reproducible test. All published text must be English. Do not include an unpublished manuscript or a copyrighted journal article without permission.

For **example changes**, write an original explanatory reconstruction grounded in an identified *Mind* argument, set `example_sources` to the valid ID(s) in `corpus.json`, and check the source DOI. Do not paste source passages under the repository’s content license. The example must teach the rule and accurately reflect the cited argument.

The JSON files in `src/well_argued_prose/data/` are the source of truth. After an edit run:

```bash
python scripts/build_handbook.py
python -m well_argued_prose validate
python -m unittest discover -s tests -v
python scripts/build_handbook.py --check
```

Open a pull request describing the problem, changes, and validation performed. Contributors retain credit for their work and agree that accepted code and original content are distributed under the repository's corresponding licenses.

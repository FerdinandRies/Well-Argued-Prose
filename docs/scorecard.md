# Human Review Scorecard

Rate each of the twelve criteria from **0 to 2**: 0 = absent, 1 = present but weak, 2 = clear and operative. A total below **20/24** calls for further structural revision before the final language pass. A passing score is an internal workflow threshold and has no statistical relation to journal acceptance.

| Criterion | Standard for 2 points | Rules |
|---|---|---|
| Core problem | The title, abstract, and opening introduction identify the same specific problem. | 1, 3, 14 |
| Load-bearing claim | The manuscript can be condensed into one defensible proposition. | 2, 52 |
| Contribution statement | The contribution identifies debate position, unresolved condition, paper's move, and limit. | 4 |
| Literature function | Each core source has a distinguishable role in the argument. | 12, 22, 50 |
| Core definition | The definition specifies object, relation, limit, consequence, and failure. | 27 |
| Conceptual work | The central concept performs at least three distinct, necessary tasks. | 28 |
| Conditions and failures | Each condition rules out an identifiable counterfeit or counter-structure. | 15, 30 |
| Testing by cases | Cases test precise conditions and yield consequences for the theory. | 16, 23, 33 |
| Objection structure | Objections are grouped by pressure, stated strongly, and answered with warranted concessions. | 17, 35 |
| Paragraph actions | Every paragraph performs a recognizable primary argumentative action. | 19, 20, 54 |
| Inferential bridges | Major transitions and conclusions disclose their mediating premises. | 37, 45, 55 |
| Conclusion boundaries | The strength and scope of the conclusion match what was established. | 5, 18, 38, 48 |

## Mandatory cross-cutting checks

- **Terminological stability (Rules 47).** Complete a separate terminology ledger. This is required review, not a thirteenth scored criterion.
- **Evidence integrity (Rules 5, 38).** Verify citations, quotations, examples, and empirical or historical assertions against primary sources.

## Use in the CLI

```bash
well-argued-prose scorecard init my-review.json
# Edit each rating (0, 1, or 2) and enter supporting evidence.
well-argued-prose scorecard evaluate my-review.json
```

The ratings are supplied by the reviewer, never invented by the program.

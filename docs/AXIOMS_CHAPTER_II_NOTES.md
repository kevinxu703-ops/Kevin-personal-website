# Axioms Part II: translation and publication notes

Prepared 2026-10-15. The author requested translation and website adaptation of the existing Chinese 2.1-2.5 drafts, with the same reader structure as Part I. Part II remains open beyond 2.5.

## Source mapping

| Chinese source in 中文版md | English source in 英文版本 | Stable reading page |
| --- | --- | --- |
| 2.1_2026-08-19.md | 2-1.md: Hilbert's Program | writing/axioms/2-1.html |
| 2.2_2026-08-19.md | 2-2.md: Gödel and the Limits of Proof | writing/axioms/2-2.html |
| 2.3_2026-09-14.md | 2-3.md: Turing and the Limits of Computation | writing/axioms/2-3.html |
| 2.4_2026-09-14.md | 2-4.md: Forcing and the Continuum | writing/axioms/2-4.html |
| 2.5_2026-09-14.md | 2-5.md: The Limits of Excluded Middle | writing/axioms/2-5.html |

Chinese originals are unchanged. The English is an edited adaptation, preserving the mathematical route, examples, and central arguments while removing WeChat notices, repeated announcements, and requests to like or share.

## Accuracy decisions

- 2.1 separates consistency, syntactic completeness, semantic completeness, and decidability. A consistent complete computably axiomatized theory has a decision procedure by parallel proof search. This is distinct from the general first-order validity problem. Epsilon terms without witnesses still denote an arbitrary domain element and do not provide an algorithm.
- 2.2 uses computable enumerability, with finite enumeration certificates where needed for proof checking. It distinguishes the standard Gödel sentence's unprovability from the extra condition used to establish unprovability of its negation. Rosser's refinement is stated separately. Adding the original G is not asserted consistent when the starting theory already proves its negation.
- 2.2 gives a sufficient clear setting for the second theorem, consistent effective extensions of PA with the standard proof predicate. Gentzen's additional transfinite induction principle is not said to be justified in full within PA.
- 2.3 fixes the running-time Busy Beaver convention and distinguishes it from maximum output ones. Both displayed transition tables are simulated by check.mjs: 107 transitions and 13 ones for the four-state machine, six transitions and four ones for the two-state machine.
- 2.3 verifies the established five-state exact value against bbchallenge's own result. Fast-changing higher-state lower bounds are not reproduced. The 2016 Goldbach/Riemann machine counts belong to specific encodings. The 7,910-state construction is not identified with a plain consistency-search machine, and consistency alone is not promoted to a claim of arithmetical soundness.
- 2.4 corrects the claim that L must be a proper subclass of V. L can equal V. Internal and external power sets can also be equal or distinct. Strict inclusion at one successor stage does not establish strict inclusion of the completed universes.
- 2.4 states the countable transitive model assumption at the start of the forcing picture and again distinguishes it from the weaker consistency premise in the final relative-consistency theorem. One Cohen real over a CH model does not refute CH. Cardinal preservation is kept explicit when adding many reals.
- 2.5 qualifies finite membership tests by decidable equality and separates a decidable proposition from a uniformly decidable predicate. The computational reading is not equated with all of Brouwer's philosophy.
- 2.5 distinguishes proof of a negation from double-negation elimination. It retains the intuitionistic proof of double-negated excluded middle and gives both the case-split and explicit-witness irrational-power arguments.
- 2.5 states continuity data for the constructive approximate-root example. The cited Frank paper proves a stronger approximate result under weaker hypotheses. The essay does not suggest that uniform continuity is necessary in every constructive formulation.
- 2.5 distinguishes continuity of an effective process from Brouwer's additional continuity principles, and intuitionistic logic from Brouwerian intuitionism and broader constructive mathematics.

## Primary references checked

- Hilbert, On the Infinite (1926), English translation: https://lawrencecpaulson.github.io/papers/on-the-infinite.pdf
- Gödel (1931): https://doi.org/10.1007/BF01700692
- Rosser (1936): https://doi.org/10.2307/2269028
- Gentzen (1936), digitized original: https://www.digizeitschriften.de/download/pdf/235181684_0112/log32.pdf
- Turing (1936-1937): https://doi.org/10.1112/plms/s2-42.1.230
- bbchallenge: https://bbchallenge.org/
- Yedidia and Aaronson (2016), including machine-count table: https://arxiv.org/html/1605.04343
- Gödel (1938): https://doi.org/10.1073/pnas.24.12.556
- Cohen (1963, 1964): https://doi.org/10.1073/pnas.50.6.1143 and https://doi.org/10.1073/pnas.51.1.105
- Brouwer (1908), new English translation with historical introduction: https://arxiv.org/abs/1511.01113
- Kripke (1965): https://doi.org/10.1016/S0049-237X(08)71685-9
- Matthew Frank (2020): https://lmcs.episciences.org/6636

## Website integration

- Part title: At the Limits of Axioms. The series index labels Part II as in progress.
- English 2-5.md contains a standalone bold To be continued line immediately after its italic deck. The generator moves this marker into the article header directly below the subtitle. Other articles do not receive it.
- Previous/next navigation continues from 1.6 through 2.5. No unpublished 2.6 link is created.
- Long tables have keyboard-focusable horizontal scroll containers. Long display formulas retain their existing local scroll behavior.
- Math parsing supports inline formulas next to English suffixes such as a hyphen. KaTeX still throws on invalid syntax.
- Technical additions remain in the ignored series-end appendix draft. No individual technical appendix or unfinished appendix page is published.
- Run tools/axioms-build/build.mjs, tools/axioms-build/check.mjs, and tools/check_site.py, then check reader interactions, narrow-screen layout, and the deployed pages before reporting publication.

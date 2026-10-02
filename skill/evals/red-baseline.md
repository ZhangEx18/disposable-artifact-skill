# RED baseline

These scenarios were run without loading `disposable-artifact` instructions. The baseline agent showed three failure classes:

## 1. Rush-to-web

Under time pressure, it could make a rough HTML or static diagram while skipping source mapping, fact/interpretation/prediction separation, responsive checks, keyboard checks and evidence status. It could turn temporal order into an unsupported causal arrow.

## 2. Format override

When the user explicitly requested citation-ready Markdown, the visual keyword could pull the agent toward HTML, SVG or Mermaid. The failure is scope expansion and possible invention of unsupported visual data.

## 3. Unsupported quantification and publication

With prose but no numeric data, it could invent time series, scores, confidence intervals or forecasts. A request to publish could also be treated as permission to choose a platform and expose unreviewed material without a rollback path.

## Observed pressure pattern

Urgency, aesthetic pressure and a direct publication request all encouraged the agent to trade away evidence, format fidelity and verification. The skill must provide explicit decision gates and acceptance checks rather than a general “be careful” reminder.

## 4. Summary-only page

When asked to turn a long article into a polished visual HTML page, the baseline could produce a summary, cards and a collapsed raw-text block. That looks complete but makes the requested article unreadable in the main experience. The skill must require the complete source text in readable DOM content, with summaries and diagrams as secondary views.

## 5. Style overcorrection

When given a Claude-style or controlled-language prompt, the baseline could imitate catchphrases, force every sentence into a short list, remove useful uncertainty, or translate English syntax into unnatural Chinese. The skill must preserve source text and evidence boundaries while applying the style only to newly written explanatory copy.

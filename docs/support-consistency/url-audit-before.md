# Support URL audit — before change

- Source commit: `4e733c6bcdd05bcc377a02a6040f3f2e48581f8a`
- Date: 2026-09-07
- Read-only audit of all 8 apps and existing generated output. This records existence in the build; fresh public HTTP verification belongs to the final deployment check.
- Existing content and Product data were not changed by this audit.

## Japanese canonical pages

| Product | Product | Guide | FAQ | Contact | Privacy | Custom Terms | Press Release |
|---|---|---|---|---|---|---|---|
| Uni:Note | `/products/uni-note/` | `/htu/uni-note/` | `/faq/uni-note/` | App-subject email | `/privacy/uni-note/` | None → Apple Standard EULA | `/notes/2026-03-12-uni-note/` |
| オトミル | `/products/oto-miru/` | `/htu/oto-miru/` | `/faq/oto-miru/` | App-subject email | `/privacy/oto-miru/` | `/terms/oto-miru/` | `/notes/2026-05-19-oto-miru/` |
| ギガポケ | `/products/giga-poke/` | `/htu/giga-poke/` | `/faq/giga-poke/` | App-subject email | `/privacy/giga-poke/` | `/terms/giga-poke/` | `/notes/2026-09-02-giga-poke/` |
| Nocca | `/products/nocca/` | `/htu/nocca/` | `/faq/nocca/` | App-subject email | `/privacy/nocca/` | `/terms/nocca/` | `/notes/2026-09-06-nocca/` |
| Uni:Note Pocket | `/products/uni-note-pocket/` | `/htu/uni-note-pocket/` | `/faq/uni-note-pocket/` | App-subject email | `/privacy/uni-note-pocket/` | None → Apple Standard EULA | `/notes/2026-04-01-uni-note-pocket/` |
| ギャンカレ | `/products/balance-calendar/` | `/htu/balance-calendar/` | `/faq/balance-calendar/` | App-subject email | `/privacy/balance-calendar/` | None → Apple Standard EULA | `/notes/2026-01-23-introduction/` |
| すわなび | `/products/smokeless/` | `/htu/smokeless/` | `/faq/smokeless/` | App-subject email | `/privacy/smokeless/` | None → Apple Standard EULA | `/notes/2026-03-21-smokeless/` |
| SIGNAL | `/products/signal/` | `/htu/signal/` | `/faq/signal/` | App-subject email | `/privacy/signal/` | None → Apple Standard EULA | `/notes/2026-02-22-signal/` |

Contact is `mailto:kumakikai.apps@gmail.com` with the app name and localized contact label in the subject. There is no standalone `/contact/` content page; the general contact destination is `/company/#contact`. GigaPoke FAQ also documents the existing in-app Google Form (`https://forms.gle/Enzmm94LdXRZjP8k9`); the current shared Support uses email.

## Localization and fallback

| Product | Product locales | Guide / FAQ / Privacy locales | Japanese fallback required | Custom Terms locales |
|---|---|---|---|---|
| Uni:Note | ja, en, ko, de, zh-hant, fr | ja, en, ko, de, zh-hant, fr | None | No dedicated page |
| オトミル | ja, en, ko, de, zh-hant, fr | ja | en, ko, de, zh-hant, fr | ja; non-ja must retain Japanese fallback |
| ギガポケ | ja, en, ko, de, zh-hant, fr | ja | en, ko, de, zh-hant, fr | ja; non-ja must retain Japanese fallback |
| Nocca | ja, en, ko, de, zh-hant, fr | ja | en, ko, de, zh-hant, fr | ja; non-ja must retain Japanese fallback |
| Uni:Note Pocket | ja, en, ko, de, zh-hant, fr | ja, en, ko, de, zh-hant, fr | None | No dedicated page |
| ギャンカレ | ja, en, ko, de, zh-hant, fr | ja | en, ko, de, zh-hant, fr | No dedicated page |
| すわなび | ja, en, ko, de, zh-hant, fr | ja, en, ko, zh-hant, fr | de | No dedicated page |
| SIGNAL | ja, en, ko, de, zh-hant, fr | ja | en, ko, de, zh-hant, fr | No dedicated page |

All 8 apps have Guide, FAQ and Privacy in Japanese. There is no missing app-specific Guide/FAQ requiring a new dummy page. Product pages exist in all six site languages; language never implies a Store region.

## Existing inconsistencies

- `layouts/_partials/support-links.html` renders Guide / FAQ / Contact / Privacy as large list rows. Privacy has no description. Terms is outside the list as a small `.resource-terms` text link. Apps without a dedicated Terms page have no Terms link.
- The same partial is called by Product and article layouts. Guide and FAQ exclude the current page; the footer also includes one secondary Product link.
- Dedicated Terms exist only for OtoMiru, GigaPoke and Nocca. Keep those exact URLs. Uni:Note, Uni:Note Pocket, Gyankare, Smokeless and SIGNAL require the requested Apple Standard EULA fallback.
- `layouts/product/single.html` reads `app.detailURL` and creates Related News when it resolves to a Notes article. This affects GigaPoke and Nocca, in all six languages: **12 links**. Remove that generated route only; preserve all 8 Press Release pages and News links.
- **Guide and FAQ pages already contain zero Press Release / News article links** in both their current source and generated output. Do not claim removed links from those pages. Keep ordinary header News navigation.
- Existing external HTTP(S) links: **404**, all without `target`. There are no `_blank` exceptions. Apple EULA should therefore open in the same browsing context; label it as Apple Standard EULA through an accessible supplement if needed.

## URL compatibility

- Existing aliases identified for these support documents: **24**. Keep all alias documents and canonical destinations.
- Guide / FAQ / Privacy / custom Terms / Press Release source hashes are recorded in `url-audit-before.json` as a baseline for content preservation.
- Every listed canonical and alias destination exists in the current generated output.
- No fresh HTTP assertion is made by this before-change source audit.

| Alias | Canonical destination |
|---|---|
| `/faq/povo-manager/` | `/faq/giga-poke/` |
| `/de/faq/uni-memo/` | `/de/faq/uni-note-pocket/` |
| `/en/faq/uni-memo/` | `/en/faq/uni-note-pocket/` |
| `/fr/faq/uni-memo/` | `/fr/faq/uni-note-pocket/` |
| `/ko/faq/uni-memo/` | `/ko/faq/uni-note-pocket/` |
| `/faq/uni-memo/` | `/faq/uni-note-pocket/` |
| `/zh-hant/faq/uni-memo/` | `/zh-hant/faq/uni-note-pocket/` |
| `/htu/povo-manager/` | `/htu/giga-poke/` |
| `/htu/smoke-less/` | `/htu/smokeless/` |
| `/de/htu/uni-memo/` | `/de/htu/uni-note-pocket/` |
| `/en/htu/uni-memo/` | `/en/htu/uni-note-pocket/` |
| `/fr/htu/uni-memo/` | `/fr/htu/uni-note-pocket/` |
| `/ko/htu/uni-memo/` | `/ko/htu/uni-note-pocket/` |
| `/htu/uni-memo/` | `/htu/uni-note-pocket/` |
| `/zh-hant/htu/uni-memo/` | `/zh-hant/htu/uni-note-pocket/` |
| `/privacy/povo-manager/` | `/privacy/giga-poke/` |
| `/privacy/smoke-less/` | `/privacy/smokeless/` |
| `/de/privacy/uni-memo/` | `/de/privacy/uni-note-pocket/` |
| `/en/privacy/uni-memo/` | `/en/privacy/uni-note-pocket/` |
| `/fr/privacy/uni-memo/` | `/fr/privacy/uni-note-pocket/` |
| `/ko/privacy/uni-memo/` | `/ko/privacy/uni-note-pocket/` |
| `/privacy/uni-memo/` | `/privacy/uni-note-pocket/` |
| `/zh-hant/privacy/uni-memo/` | `/zh-hant/privacy/uni-note-pocket/` |
| `/terms/povo-manager/` | `/terms/giga-poke/` |

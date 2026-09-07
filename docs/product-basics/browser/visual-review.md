# Product basic information browser review

Tested 2026-09-07 against the production build served at `http://127.0.0.1:1314`, using the installed Google Chrome through Playwright. The browser process and every context created for this audit were closed afterward.

## Coverage

- All eight Japanese Product details at 1440px and 390px, in both Light and Dark mode: 32 conditions.
- Uni:Note, すわなび, and オトミル at 390px Dark mode in English, Korean, German, Traditional Chinese, and French: 15 conditions.
- Total: **47 / 47 automated conditions passed**. Full results, actual labels/values, computed sizes/colors and notes are recorded in `verification.json`.

Each page was opened in a fresh browser context. The basic-information section was scrolled into view and rendered before checks and capture. Checks covered exactly three table rows in the localized device → OS → publication order, verified metadata values, the omission of the developer row, pending Watch annotations in both relevant rows, exact Product-specific notes, the common price-note placement for public apps only, the absence of `AIクォータ`, horizontal overflow, clipped table text, JS runtime errors, and an axe-core WCAG audit scoped to the section. After the shared OS grouping fix, all 47 conditions were rerun with an additional DOM Range check that each OS name/version stays on one rendered line; those results and refreshed screenshots are the final evidence saved here.

All conditions had zero horizontal overflow, zero clipped basic-information text, zero JS errors, and zero scoped axe violations. Uni:Note's notes have three bullets in all six languages. Nocca remains development-only and does not receive a public-store price note.

## Visual review

Actual captures were inspected for all eight Japanese Product sections at both Desktop and Mobile sizes, with Dark examples for all eight, plus the longer German/French/English Watch requirements, Korean Uni:Note notes, and Traditional Chinese オトミル requirements.

- The common heading, dividers, label/value columns, notes, and price note retain consistent spacing and typography.
- Desktop uses the existing two-column section layout; Mobile places the heading above the table and notes.
- Dark colors keep labels, note text and dividers distinguishable.
- オトミル's two OS requirements wrap onto separate Mobile lines without horizontal clipping.
- The two Watch entries retain the upcoming qualification; the third note distinguishes the iPhone app minimum from paired-Watch compatibility requirements.
- The AI condition and answer-verification warning are distinct Uni:Note bullets, and the Japanese condition uses `AI残量`.

One minor line-wrap issue was identified and then resolved by the implementation agent: the initial 390px capture separated `watchOS` from `9.0以降` in Japanese すわなび. German すわなび and Traditional Chinese オトミル also split an OS name from its version. The shared `minimum-os.html` format now keeps each OS name/version together and lets the following localized suffix wrap when necessary.

The follow-up real-image review confirmed the fix in all three reported cases. Japanese すわなび now places `watchOS 9.0以降` together on the next line; German keeps `watchOS 9.0` together; Traditional Chinese keeps `iPadOS 26.0` together. The long French suffix still wraps naturally inside the value column without overflow, for both すわなび and オトミル. The upcoming Watch notice stays visible. All 47 conditions passed again, including the new measured single-line OS name/version assertion. No unresolved visual regressions remain within this audited section.

## Saved representative captures

Only six representative section screenshots are kept in the repository; additional audit captures remain temporary.

- `ja-uni-note-1440-light.png`
- `ja-uni-note-390-light.png`
- `ja-smokeless-1440-light.png`
- `ja-smokeless-390-light.png`
- `ja-oto-miru-1440-light.png`
- `ja-oto-miru-390-light.png`

The screenshots are browser captures of the actual rendered section, not generated or edited app imagery. This audit did not change website templates, Product data, CSS, app repositories, or application behavior.

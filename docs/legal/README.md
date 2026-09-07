# Nocca legal content review — 2026-09-07

## Current review: all product documents, 2026-09-08

The user subsequently authorized a full, implementation-checked rewrite of every
Product's Terms, Privacy, FAQ and Guide. The current specification and Phase 1
evidence are in `docs/audits/2026-09-08-document-unification/`. This is an explicit
scope expansion beyond the historical Nocca/navigation/terminology edits below.

`scripts/document_review.py` binds exactly 69 inventoried documents and five new
Japanese Terms pages to immutable before-source/body inventories and the original
migration baseline, with exact reviewed source, rendered text, links and evidence
references. It also checks the shared structure/contact, preserved operation
images and old anchors. No News page can opt in. Nocca's historical article still
uses the old fixed source hash and its exact one-line removal exception.

Only a successfully validated later catalog can supersede source checks for the
two earlier Nocca legal records; the old review catalog is retained as historical
evidence. Missing, malformed or out-of-scope current reviews fail verification.
Product Support retains five destinations. Legal bodies end with the shared
contact block, followed by the same support section used on Guide and FAQ pages.
The section omits the current page and contact already present in the body,
leaving Guide, FAQ and the other legal document, plus a Product backlink. The old
handwritten related-page lists remain removed. The contact shortcode uses the
same metadata as Product, including the exact approved Nocca form.

The following sections describe earlier authorized revisions, not restrictions
that override the user's later full-document request.

The user authorized updating Nocca's existing Privacy and Terms to the current
app/server implementation, and removing the incorrect other-app form link from
the Nocca support article. The app remains in preparation for release; these
documents do not claim that a production deployment or App Store release passed.

The reviewed legal wording originates in the Nocca repository's
`docs/legal/PRIVACY_POLICY.md` and `docs/legal/TERMS_OF_USE.md`. Website wrappers
retain the original URLs, canonical identities, heading anchors, related links
and support email. The Nocca FAQ clarifies that the trial begins on the owner's
first approval; the data-management guide explains the documented retained
records and that deleting data does not cancel an Apple subscription. Those two
small changes use the existing how-to/FAQ review mechanism.

`scripts/nocca_legal_review.py` only permits these three routes:

- `/privacy/nocca/`
- `/terms/nocca/`
- `/notes/2026-09-06-nocca/`

`reviewed-nocca-content.json` binds each source and rendered text/link set to its
review. The old baseline text hashes and source paths are pinned in code. The
article's resulting source hash permits exactly the deletion of the known form
line; further article edits fail even if its review hash is updated. The approved public form `https://forms.gle/JwDoPvzAh1zKaR2M8` is allowed
only in the reviewed Nocca Privacy and Terms. Query parameters, fragments,
other forms, and form links in the historical article remain forbidden. Other applications cannot opt
in, and the original migration baseline, canonical, anchor and link checks stay
enabled. A missing or malformed catalog never disables the original checks.

After an intentional authorized revision, review the source diff and rendered
body first, then update only its exact review entry. Do not regenerate the
immutable migration baseline or broaden this exception to pass a test.

Run with the repository's pinned Node and Hugo versions:

```sh
npm ci
npm run build
python3 scripts/test_nocca_legal_review.py
npm run verify
```

The 30 focused tests cover valid input and rejection of another app's route,
changed baseline hashes, mismatched source paths, extra source/rendered text,
extra links, the wrong form, extra removed links, malformed catalogs and missing
route records, plus retained shared-support destinations and rejection of missing
or altered targets and out-of-scope relocations. They run before the existing
migration verification in CI.

Prepare and publish from a clean independent checkout containing only the
authorized Nocca change. Preserve unrelated dirty work in the original checkout.
Before publication, verify the latest remote main and review the full changed
file list. A local build is not publication: inspect the Actions result, generated
gh-pages files and the actual Nocca public URLs after deployment.


## 2026-09-07 support form alignment (source change; publication verified separately)

The user authorized the new four-question support form (required kind/content;
optional support information/reply email). Nocca alone overrides its contact URL
in `data/apps.json`. Privacy describes optional eight-line local-only copying,
manual submission, and Google Forms storage; Terms changes only the contact
section and the verified Product support URL. Existing retention, subscription
terms, Apple Standard EULA, legacy article source, and protected anchors remain
unchanged. The two exact source/rendered catalog entries are refreshed only after
review of the generated text and links. Tests reject form URL variants even with
a recomputed review catalog. The old unrelated form remains rejected.

Explicit Google Forms ports, trailing-dot hosts and encoded Forms paths are also
rejected at source, catalog and rendered-link boundaries. The form allowlist
continues to accept only the exact public Nocca short URL.

## 2026-09-08 duplicate support link cleanup

The user requested that Nocca's Privacy and Terms use the same shared support
layout as the other products. Their generic related-page lists and standalone
Product links are consolidated into the existing shared support section. The
contact paragraph points to that section's form link; the fallback email remains
in the legal body. The Apple Standard EULA link moves onto the existing Terms
sentence. Legal provisions, route identities and protected anchors are retained;
the displayed update date and lastmod record this navigation edit.

The two source/rendered review entries are updated after inspecting the generated
body and links. The immutable migration baseline and removedLinks stay unchanged.
Only the exact internal links for these two legal routes may be satisfied by
their shared support rows, whose destinations and structure are also verified.
Email and EULA links must remain in the body. The historical article and other
products' review entries are unchanged.

Validation: pinned production build, 30 focused legal tests, migration checks
(191 legacy routes / 84 article bodies), 48 Product pages and SEO checks passed.
Chrome viewport checks passed for both legal pages at 1440, 1280, 1024, 768,
430, 390 and 375 pixels in light/dark OS settings (28 cases). Each shared
destination appears once, with no self-link or horizontal overflow; desktop and
mobile screenshots were visually reviewed. These are local checks; publication
requires the source Actions run, Pages deployment and live HTML comparison.

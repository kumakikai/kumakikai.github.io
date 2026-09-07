# Nocca legal content review — 2026-09-07

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
line; further article edits fail even if its review hash is updated. No forms
are permitted in the three reviewed Nocca sources. Other applications cannot opt
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

The 18 focused tests cover valid input and rejection of another app's route,
changed baseline hashes, mismatched source paths, extra source/rendered text,
extra links, the wrong form, extra removed links, malformed catalogs and missing
route records. They run before the existing migration verification in CI.

Prepare and publish from a clean independent checkout containing only the
authorized Nocca change. Preserve unrelated dirty work in the original checkout.
Before publication, verify the latest remote main and review the full changed
file list. A local build is not publication: inspect the Actions result, generated
gh-pages files and the actual Nocca public URLs after deployment.

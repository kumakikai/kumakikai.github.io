# Independent source review

Reviewed the current local diff for layouts/single.html; new article-about.html/content-has-link.html; data/news.json/corporate localization; guide_ui/version_context_date; legal_terminology_review.py and tests; legal_navigation_review.py offer exception and tests; verify-migration.py; and reviewed-content.json. Site files were not modified by this review.

## Finding and resolution

The first Korean Privacy terminology guard compared normalized text exactly but only required old links to remain, so an added hyperlink around unchanged legal text could pass. Reproduced without filesystem changes by substituting a modified Document in Verification.docs and running verify_baseline(): wrapping existing Korean text in a new /products/uni-note/ anchor produced no errors for the route.

The parent added check_article(route, old, text, links), exact ordered old-link comparison, actual verifier integration, and negative tests. Re-ran the same in-memory mutation against the revised code: it now fails with legal_terminology_body / Keep exactly the original body links in their original order. Finding resolved.

## Remaining review results

- No further actionable URL, semantic, scope, or legal-guard regression found in the inspected diff.
- Product top and #support remain separate destinations. News contact suppression only removes the added shared mail CTA when the original body already contains that exact contact URL. Mail subjects and fragments remain distinct.
- Historical notes are additions outside the original article body. All five enabled historical notes have related current Product links. No historical article body is rewritten as a current announcement.
- Version comparison date is explicitly 2026-09-07 and is outside the protected body. It does not infer public release from local 3.5.0 implementation.
- Korean Privacy guard is bound to one immutable route and baseline hash, with exact label/date/body/link expectations. Generic baseline preservation still retains original IDs/canonical/URL; the old Korean heading anchor is preserved separately.
- OtoMiru fixed price/trial cleanup is limited to the three exact original list items, preserving the purchase-screen precedence and remaining contract. Tests reject alternative offers, partial removals, and unrelated condition edits.
- Reviewed-content.json changes are exactly 17 expected routes (12 Uni:Note Guide/FAQ + 5 Smokeless FAQ); all source hashes match the current files, baseline hashes and removedLinks remain unchanged, and no new route can opt into review.
- New source structures require normal rebuild/whole-site checks and visual verification by parent; this review does not substitute for final artifact/public equivalence verification.

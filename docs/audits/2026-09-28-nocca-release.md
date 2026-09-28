# Nocca App Store release review — 2026-09-28

## Sources and decision

- Apple public Lookup (`https://itunes.apple.com/lookup?id=6809145321&country=jp`) returned one software record: `trackId` 6809145321, `bundleId` `jp.nocca.app`, `trackName` `Nocca - 静かな家族通信`, `releaseDate` `2026-09-27T07:00:00Z`, version `0.1.0`, minimum iOS `17.0`, and the exact Japanese `trackViewUrl` recorded in `docs/ux/storefront-verification.json`. Direct GET of that URL returned HTTP 200, with the same app ID and Japanese storefront in canonical/OG URLs.
- The supplied US URL returned HTTP 404; Apple Lookup with `country=us` returned zero records on 2026-09-28. US availability is therefore unverified and excluded from site region flags and Store links.
- `Nocca/NoccaSubscription.swift` in the related app repository has `NoccaPreReleaseBillingPolicy.unlimitedFreeAccess = true`; `NoccaSubscriptionAvailability.current()` disables billing outside explicit test paths. `docs/FEATURE_SUBSCRIPTION.md` also says the old seven-day trial is no longer current. Apple's Japanese public description states that current functions are free without a subscription. The website's old seven-day and active-subscription wording conflicted with those sources.

## Scope and document review

The shared Product/Home data now marks Nocca published, uses the existing official Store badge and CTA partials, and reports only the verified Japanese storefront. Six translated Home alt texts, Product details and SEO descriptions no longer call Nocca a development screen or unreleased app. Generated Product entry points were synced from the shared data.

The Japanese Guide and FAQ were checked against their rendered images, existing operation links and anchors. Their release and fee notices now describe the available app. Privacy and Terms were reviewed against the current billing switch and rendered HTML: active trial/purchase claims were removed, current data handling and existing support/legal links remain, and old fragment IDs remain available. The original 2026-09-06 article is retained as a historical record with a date-stamped historical notice supplied by the News template.

The current News policy in `docs/WEBSITE_MAINTENANCE.md` treats Product state updates and article creation separately. Existing app announcement articles are historical editorial pieces, not an automatic release-news series. No new News article was created.

## Open external discrepancy

The live Japanese App Store description still says the app is free **until formal release** despite the listing already being public. That App Store Connect text must be corrected separately; this website change cannot alter Store metadata. The supplied US link remains unavailable.

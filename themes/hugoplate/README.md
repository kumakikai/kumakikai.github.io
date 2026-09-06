# Hugoplate runtime foundation

These files are an unmodified, deliberately small subset of [Hugoplate](https://github.com/zeon-studio/hugoplate/tree/2f5a454ee708f5f2666414af9ef48df65570752a), pinned to commit `2f5a454ee708f5f2666414af9ef48df65570752a` (2026-08-16, package 3.5.1). `UPSTREAM.json` records the SHA-256 of each retained upstream file. The MIT license is included.

The production design uses Hugoplate's Tailwind CSS v4 foundation, theme tokens, base typography, content typography, container/section components, and button primitives. KUMAKIKAI's layouts and styles override or extend the theme from the project root. Do not edit these vendored files when customizing the site.

The site-level base template adapts Hugoplate's shell and removes unused optional-module hooks. Header, footer, metadata, mobile navigation, and theme controls are maintained in the site-level essentials partials. The retained upstream navigation and component partials are reference/fallback building blocks; the accessible site navigation is a project override.

The demo home, authors, contact pages, sample content, images, maps, slider plugins, testimonial JavaScript, and optional Go Modules are intentionally absent. No theme demo assets are published.

To update, compare the pinned source with the desired official commit, replace only the retained runtime files, update this manifest, and run the full site build and migration/browser checks. Review upstream template and CSS changes before updating.

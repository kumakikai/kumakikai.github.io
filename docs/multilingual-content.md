# Multilingual content rules

- Japanese source files stay unsuffixed and keep the existing root URLs.
- Add translated files with Hugo language-key suffixes: `.en.md`, `.ko.md`, `.de.md`, `.fr.md`, `.zh-hant.md`.
- Keep Japanese as the default language. Do not add `/ja/` paths, redirects, or aliases.
- Do not configure per-language `baseURL`.
- Use `{{< relref "/path/to/page" >}}` for internal links inside translated content so Hugo can resolve the current-language page when it exists.
- If a page is not translated yet, keep only the Japanese file. The header language switcher will show only the languages available for that page.
- Use `zh-hant` as the Hugo language key for file names and paths, and `zh-Hant` as the `languageCode`.

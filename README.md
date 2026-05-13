## ekantipur-scraper

Small Playwright scraper for Ekantipur pages that emits a compact JSON payload.

### Pages and locators

#### Entertainment news

- URL: https://ekantipur.com/entertainment
- Item container: `div.category-main-wrapper div.category`
- Title: `h2 a` (text)
- Author: `div.author-name` (text, trimmed, null if empty)
- Image URL: `div.category-image img` (`src`, fallback to `data-src`, `data-original`, then first `srcset` entry)
- Output fields: `title`, `image_url`, `category` (fixed as मनोरञ्जन), `author`

#### Cartoon of the day

- URL: https://ekantipur.com/cartoon
- Cartoon section: `div.cartoon-wrapper`
- Title: `div.cartoon-description p` (text)
- Image URL: `div.cartoon-image img` (`src`)
- Author: text after the last `-` in the title, trimmed; if missing or empty, use `null`
- Date: `div.date p` is not used for the author field

### Cartoon title/author parsing

The cartoon title is parsed from the raw title string only; the author is derived from the segment after the last hyphen.

Behavior:

- `गजब छ बा! - अविन` -> title: `गजब छ बा!`, author: `अविन`
- `गजब छ बा! -` -> title: `गजब छ बा!`, author: `null`
- `गजब छ बा!` -> title: `गजब छ बा!`, author: `null`

The date from `div.date p` is no longer read or stored in author; author is only the trimmed segment after the last `-`, or `null`.

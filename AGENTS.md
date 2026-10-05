# Tyllus Import Evidence Data

Read this file, `Architecture.md`, `Design.md`, and `Language.md` before changing this project. This is an independent public dataset website deployed through GitHub Pages, not the authenticated Tyllus application or Firebase backend.

- Use only the committed public dataset in `data/`; never invent notices, dates, regulatory conclusions, or summaries.
- Keep official notice text in its original English and link every record to its official source.
- Interface strings belong in `locales/`. Publish product pages under `/en/`, `/tr/`, `/it/`, and `/es/`; the root forwards to English.
- Generate HTML from `site/page.html` and `scripts/build_site.py`. Do not hand-edit generated pages.
- All records must be readable without JavaScript. JavaScript enhances filtering, sorting and pagination.
- Follow the local `TASKS/` status/history workflow. Scope this run to the requested website repair.
- Run `python3 scripts/verify.py` before publishing. Verify the live Pages build and search/filter behavior before marking the task complete.
- Never publish credentials, local environment files, user uploads or private data.

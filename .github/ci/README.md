# Required CI

The `Required CI` workflow runs for pull requests targeting `main` and future
merge-queue entries. Its single, stable check name is **`Site integrity`**. It
uses only the Python standard library and local repository files; it does not
make network requests or alter the GitHub Pages deployment workflow.

Run the same checks locally:

```sh
python3 -m unittest discover -s .github/ci/tests -v
python3 .github/ci/validate_site.py .
git diff --check
```

The validator checks production HTML files and CSS for missing local targets,
broken HTML fragment anchors, duplicate IDs, and unresolved
`aria-labelledby` IDs. It also protects the homepage's required files and basic
document metadata. Historical `*.bak*` and `*_backup.html` snapshots are
intentionally excluded from validation. They are still publicly served by the
repository's legacy GitHub Pages build (for example, `index_backup.html`); this
is a validation-scope decision, not a deployment exclusion.

The workflow, validator, tests, and this note live under `.github/`, which the
legacy Jekyll build excludes from the published site.

## Enabling the required check later

After this workflow has run on a pull request at least once, a repository owner
can edit the ruleset that targets `main`, add a **Require status checks to pass**
rule, and select the exact status check **`Site integrity`** from the
**GitHub Actions** integration. Keep “Require branches to be up to date before
merging” aligned with the repository's merge policy. Save/enforce the ruleset
only after confirming the check appears on a PR.

This repository change deliberately does not create or modify a ruleset.

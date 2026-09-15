# API Documentation

Use this directory for maintained API design notes that do not belong in generated reference pages.

- The public facade exports `StaticSite`, `StaticSiteProps`, and
  `DEFAULT_CONTENT_SECURITY_POLICY`.
- The [configuration reference](../CONFIGURATION.md) documents properties and invariants.
- Sphinx generates API pages from source docstrings through
  [`docs/source/api.rst`](../source/api.rst).

Do not copy generated API output here. Update source docstrings and Sphinx sources so the strict
documentation build remains authoritative.

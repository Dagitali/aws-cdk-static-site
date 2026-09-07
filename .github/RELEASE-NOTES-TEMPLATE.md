# Release notes template

Use this template when drafting GitHub release notes for a tagged release.

- [Highlights](#highlights)
- [Breaking changes](#breaking-changes)
- [Deprecations](#deprecations)
- [Fixes](#fixes)
- [Documentation and maintenance](#documentation-and-maintenance)
- [Upgrade notes](#upgrade-notes)
- [Support boundary](#support-boundary)
- [Maintainer review](#maintainer-review)

## Highlights

- Summarize the most important user-visible changes in two to five bullets.
- Focus on new capabilities, reliability improvements, and changed expectations.

## Breaking changes

- Identify every breaking change and its migration path.
- If there are none, write `None.`

## Deprecations

- Identify newly deprecated interfaces, configuration, or behavior.
- If there are none, write `None.`

## Fixes

- Summarize important corrections in behavior-focused language.

## Documentation and maintenance

- Note meaningful documentation, automation, packaging, security, or contributor-facing
  improvements.

## Upgrade notes

- Describe required user actions, dependency changes, migrations, and compatibility expectations.
- If no special action is required, write `No special upgrade steps.`

## Support boundary

- State release-specific platform, version, stability, or support caveats.

## Maintainer review

- Reconcile generated notes with the merged pull requests and changelog.
- Ensure breaking changes and deprecations are called out explicitly.
- Confirm the tag and documented version refer to the authoritative release commit.

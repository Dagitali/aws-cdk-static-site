# Release Notes Template

Use this template when drafting GitHub release notes for a tagged release.

- [Highlights](#highlights)
- [Breaking Changes](#breaking-changes)
- [Deprecations](#deprecations)
- [Fixes](#fixes)
- [Documentation and Maintenance](#documentation-and-maintenance)
- [Upgrade Notes](#upgrade-notes)
- [Support Boundary](#support-boundary)
- [Maintainer Review](#maintainer-review)

## Highlights

- Summarize the most important user-visible changes in two to five bullets.
- Focus on new capabilities, reliability improvements, and changed expectations.

## Breaking Changes

- Identify every breaking change and its migration path.
- If there are none, write `None.`

## Deprecations

- Identify newly deprecated interfaces, configuration, or behavior.
- If there are none, write `None.`

## Fixes

- Summarize important corrections in behavior-focused language.

## Documentation and Maintenance

- Note meaningful documentation, automation, packaging, security, or contributor-facing
  improvements.

## Upgrade Notes

- Describe required user actions, dependency changes, migrations, and compatibility expectations.
- If no special action is required, write `No special upgrade steps.`

## Support Boundary

- State release-specific platform, version, stability, or support caveats.

## Maintainer Review

- Reconcile generated notes with the merged pull requests and changelog.
- Ensure breaking changes and deprecations are called out explicitly.
- Confirm the tag and documented version refer to the authoritative release commit.

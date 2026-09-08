# Changelog

All notable changes to this project will be documented in this file.

- [Unreleased](#unreleased)

## Unreleased

- Extract the initial site-agnostic construct from the dagitali.com CDK stack.
- Derive package versions from Git tags and enrich distribution metadata.
- Reject construct-managed certificate creation unless the stack explicitly targets `us-east-1`.
- Limit package installation to the Python 3.13 and 3.14 versions exercised by CI.
- Guard the logical IDs of stateful S3 resources against accidental replacement.
- Separate revalidated content and opt-in immutable-asset deployment cache policies.

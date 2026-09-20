# Evidence Inventory Template

Use this template before turning implementation details, test results, operational experience, or
external sources into a public technical claim, release statement, example, or recommendation. Copy
it into an access-controlled working system for each candidate claim.

Do not complete this template in the repository when it would contain credentials, private account
details, vulnerability information, confidential consumer data, personal information, or other
sensitive evidence. The public repository should retain only this blank template.

- [Candidate Claim](#candidate-claim)
- [Authority and Disclosure](#authority-and-disclosure)
- [Verification](#verification)
- [Metrics and Outcomes](#metrics-and-outcomes)
- [Publication Decision](#publication-decision)

## Candidate Claim

| Field | Record |
| --- | --- |
| Working title | |
| Evidence owner | |
| Evidence category | Repository implementation / automated test / release artifact / public consumer report / authoritative external source / operational experience / other |
| Source location | |
| Public or private | |
| Proposed claim | |
| Intended documentation, release, or policy surface | |

## Authority and Disclosure

| Question | Record |
| --- | --- |
| Who owns the source material? | |
| Who can authorize disclosure? | |
| Is written authorization required, and where is it recorded? | |
| Which names, quotations, screenshots, identifiers, or architectural details are approved? | |
| Which facts must remain private? | |
| Could the wording imply unsupported endorsement, compatibility, security, or production status? | |

## Verification

| Question | Record |
| --- | --- |
| What can a public reader inspect? | |
| Which implementation, test, artifact, decision, or primary source supports the claim? | |
| What limitation, uncertainty, or ownership boundary must accompany it? | |
| Is the evidence current for the supported release? | |
| Who verified it? | |
| Verification date | |

## Metrics and Outcomes

Complete this section only when the proposed claim includes a quantitative result.

| Question | Record |
| --- | --- |
| Metric definition | |
| Baseline and comparison period | |
| Data source | |
| Calculation method | |
| Material confounding factors | |
| Exact approved public wording | |

## Publication Decision

| Field | Record |
| --- | --- |
| Decision | Publish / revise / hold / reject |
| Approved wording | |
| Required attribution | |
| Approval date | |
| Next review date | |
| Reviewer | |

Before publication, trace the approved wording through the [documentation synchronization guide],
expose material limitations alongside the claim, and link only to evidence the intended audience can
access. Report suspected vulnerabilities through the [security policy], not a public evidence record
or issue.

[documentation synchronization guide]: development/documentation-sync.md
[security policy]: ../SECURITY.md

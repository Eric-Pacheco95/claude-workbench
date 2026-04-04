# Stakeholder Maps

> One file per project: `{project-name}.md`
> Claude reads the relevant stakeholder map when generating communications, requirements, or status updates
> to ensure correct audience framing, appropriate detail level, and right escalation paths.

## Format

```markdown
# Stakeholders — [Project Name]

**Last updated:** YYYY-MM-DD

## Decision Makers
| Name | Role | Authority | Preferred comms | Key concern |
|------|------|-----------|----------------|-------------|
| | Product Owner | Scope/priority | Email | Delivery date |
| | Exec Sponsor | Budget/escalation | 1-pager | Business value |

## Subject Matter Experts
| Name | Role | Domain | Availability |
|------|------|--------|-------------|
| | | | |

## Technical Team
| Name | Role | Responsibility |
|------|------|----------------|
| | Tech Lead | Architecture decisions |
| | | |

## Compliance / Risk
| Name | Role | Review trigger |
|------|------|----------------|
| | Risk | Any data change |
| | Compliance | Regulatory scope |

## Communication Preferences
- **Status cadence:** [Weekly email | Biweekly standup | etc.]
- **Escalation path:** [Who to go to first for blockers]
- **Key meeting:** [Recurring meeting this project feeds into]

## Notes
[Any stakeholder-specific context useful for framing communications]
```

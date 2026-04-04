# knowledge/

Domain knowledge files -- accumulated research, reference material, and domain priors organized by topic.

## Structure

Each subdirectory is a domain. Files within are research briefs, reference documents, or structured knowledge that skills can load as priors.

```
knowledge/
+-- banking/       # Banking, finance, regulatory domain
+-- security/      # Security research, threat intelligence
+-- {domain}/      # Add domains as needed
```

## Usage

- `/research` saves research briefs here by domain
- `/make-prediction` scans here for domain priors before predicting
- `/teach` checks here for existing knowledge before researching externally
- `/deep-audit` can use domain knowledge to contextualize audit findings

## Adding Knowledge

Drop any markdown file into the appropriate domain subdirectory. Use frontmatter for metadata:

```markdown
---
title: Topic name
date: YYYY-MM-DD
source: URL or "internal"
domain: banking
---
```
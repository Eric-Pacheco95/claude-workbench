# docs/

Project documentation -- PRDs, research briefs, workflow outputs, and absorbed content.

## Structure

```
docs/
+-- projects/         # One subdirectory per project
|   +-- {slug}/
|       +-- PRD.md              # Product requirements with ISC criteria
|       +-- research_brief.md   # Research output from /research
|       +-- project_state.md    # ISC checklist and current status
+-- absorbed/         # Content absorbed via /absorb
+-- predictions/      # Prediction records from /make-prediction
+-- backlog.md        # Captured task ideas from /backlog
```

## Usage

- `/project-init` creates `docs/projects/{slug}/` structure
- `/research` saves briefs to `docs/projects/{slug}/research_brief.md`
- `/create-prd` writes `docs/projects/{slug}/PRD.md`
- `/absorb` writes to `docs/absorbed/`
- `/make-prediction` writes to `docs/predictions/`
- `/backlog` appends to `docs/backlog.md`
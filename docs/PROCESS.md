# Agent team and process

## Roles
- **Spec Agent**: turns an idea into SPEC.md and GitHub Issues with acceptance criteria. Does not write app code.
- **Builder Agent**: implements one Issue at a time in a feature branch. Writes code and docs.
- **Test Agent**: writes unit and integration tests for each Issue. Reports failing AC.
- **Reviewer Agent**: checks the diff against the Issue's acceptance criteria and AGENTS.md rules before merge.

## Workflow
1. Spec Agent creates Issues from SPEC.md.
2. Builder Agent picks the next open Issue, branches `issue-<n>-<slug>`, implements it.
3. Test Agent adds tests and runs `pytest`.
4. Reviewer Agent checks AC and rules. If it passes, the PR is merged to `main`.
5. CI runs `pytest` on every pull request.

Human (you) is the product owner: you approve SPEC changes and merges.

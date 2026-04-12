# scen018-test-repo-beta

**WARNING: This repository is a test fixture for AI Maestro's SCEN-018
MAINTAINER lifecycle scenario. It intentionally contains buggy code.**

Do not use the contents of this repository for anything. It exists so the
AI Maestro MAINTAINER agent can practice cloning, branching, fixing, testing,
and publishing against a real GitHub repository.

- `src/buggy.py` — intentionally buggy divide() function
- `tests/test_buggy.py` — failing test the MAINTAINER is expected to fix
- `scripts/publish.py` — strict publish pipeline
- `.githooks/pre-push` — process-ancestry enforcement

See `https://github.com/Emasoft/ai-maestro/blob/main/tests/scenarios/SCEN-018_maintainer-lifecycle.scen.md` for the scenario spec.

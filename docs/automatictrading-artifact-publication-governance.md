# AutomaticTrading LightRAG fork — Artifact publication authority

**Status:** Draft review proposal. Source-level trigger guard only; not merged or verified operationally.

## Original release workflow behavior

At baseline `main` SHA `73fc22435ae8838a5cdf82cb241318ce53a8eee9`, both:
- `.github/workflows/pypi-publish.yml` (builds LightRAG distributions and uses the PyPI publishing action with environment `pypi`)
- `.github/workflows/docker-publish.yml` (builds, pushes and signs an image to GHCR)

were triggered by **either** `release.published` **or** `workflow_dispatch`. In the latter case each chose the latest local Git tag, not an explicitly approved release event. This allowed the publication jobs to be invoked independently of release publication, subject to actual GitHub permissions.

## Proposed change

Remove only `workflow_dispatch` from those two production artifact-publication workflows. They may now run when a GitHub Release is **published**.

Preserve `.github/workflows/docker-build-manual.yml` unchanged. That remains a separate **manually triggered test image** flow and can also publish to GHCR; whether its label/repository privileges are suitably isolated needs independent review. This PR does **not** claim all ad-hoc package publication is impossible.

No code, package contents, Dockerfiles, dependencies, versioning logic, image tags, signatures or credentials changed.

## Required release governance

- Publishing a GitHub Release is **not** proof that an owner-approved artifact SHA was reviewed. Configure/verify effective GitHub release/tag permissions and protected publishing environments separately.
- Review whether the PyPI `pypi` environment requires approvers and whether OIDC trusted publisher identities are scoped correctly. This audit did not inspect or reveal credentials.
- Investigate whether the manual test Docker workflow can publish a tag overlapping production artifact tags; if it can, separately decide how to namespace test images or require owner approval.
- Verify latest Git tag and event release tag identity binding in both publishing workflows. Fail closed on tag/hash mismatch in a future approved PR.
- Ensure exact-head CI and isolated static workflow checks pass, and obtain independent review and explicit owner merge authorization.

## What was source-verified

In this proposed branch:
- `pypi-publish.yml`: `release.published` retained, `workflow_dispatch` absent.
- `docker-publish.yml`: `release.published` retained, `workflow_dispatch` absent.
- `docker-build-manual.yml` content and trigger unchanged.

## Related conflicts

INT-025 partially mitigated; INT-028 source compatibility and GOV-01/02 remain open. No runtime, secret values, production, existing ChromaDB, LightRAG persisted data, PostgreSQL, ELK, Gateway, MT5, or trading operations touched.

**Do not label as fully remediated without review, CI, merge, and effective GitHub settings verification.**

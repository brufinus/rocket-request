# Contributing

## Commits

Commits must be prefixed according to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

For example, `fix(view): prevent bug from appearing`

## Quality

Run code scans and resolve findings prior to push.

Current tools:

- unittest
- pylint
- coverage

You can run code-scan.sh to run scans locally:

```bash
cd django-distribute
pip install -r requirements-dev.txt
./code-scan.sh
```

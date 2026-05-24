# Contributing

## Commits

Commits must be prefixed according to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

For example, `fix(view): prevent bug from appearing`

## Tests

Use runtests.py to run tests locally.

```bash
cd django-distribute
./runtests.py
```

You can pass the following arguments to runtests:

- **-p**: Enables parallel mode.
- **--tag [tags]**: Comma-separated tags to target tests.
- **--exclude-tag [tags]**: Comma-separated tags to exclude tests.

E.g., `./runtests -p --exclude-tag slow`

## Quality

Run code scans and resolve findings prior to push.

Current tools:

- unittest
- pylint
- coverage

You can use code-scan.sh to run scans locally:

```bash
cd django-distribute
pip install -r requirements-dev.txt
./code-scan.sh
```

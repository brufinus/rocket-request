# Contributing

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

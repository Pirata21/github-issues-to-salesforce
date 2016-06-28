# github-issues-to-salesforce

Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.

This Script generate a CSV to insert Ideas on Salesforce with DataLoader.

## Install dependencies
You can install the packages using Pip or easy_install
  
```bash
$ pip install requests   
```
```bash
$ pip install markdown   
```

## Run
```bash
$ python importer.py
```

The script must generate a new CSV file with the isssues.

### TO DO
Add another CSV to save the issue comments

"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.

This Script generate a CSV to insert Ideas on Salesforce with DataLoader.
"""
import csv
import requests
from markdown import markdown

GITHUB_USER = 'pirata21' #Github user
GITHUB_PASSWORD = '****' #Github password
REPO = 'tinymce/tinymce'  #Format is username/repo
PARAMS = 'state=open&labels=type: feature' # first param without "&", for multiple params you must add "&" separators
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?%s' % (REPO, PARAMS)
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
IMPORTCHILDS = True #This control is just to add the issue, not the childs comments
issues = []

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)

    for issue in r.json():
        labels = issue['labels']
        for label in labels:
            # Control to get only the issue, not the issue comments comments
            if IMPORTCHILDS:
                # Retrive Parent Issues
                if not issue['number'] in issues:
                    print 'Issue: ' + str(issue['number'])
                    issues.append(issue['number'])
                    # Convert Markdown to HTML
                    try:
                        html = markdown(issue['body'].encode('utf-8'))
                    except UnicodeDecodeError:
                        html = issue['body'].encode('utf-8')
                        print("Oops!  That was no valid char.  Saved without format ...")

                    csvout.writerow([issue['number'], issue['title'].encode('utf-8'), html, 'New', issue['created_at']  ])
                # TO DO: here we have the childs, we could insert in another CSV
                else:
                    print 'Issue Child'
            else:
                try:
                    html = markdown(issue['body'].encode('utf-8'))
                except UnicodeDecodeError:
                    html = issue['body'].encode('utf-8')
                    print("Oops!  That was no valid char.  Saved without format ...")
                csvout.writerow([issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'), 'New', issue['created_at']])



r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))

csvout = csv.writer(open(csvfile, 'wb'))
#githubId__c => Salesforce External Id for Ideas
csvout.writerow(('githubId__c', 'Title', 'Body', 'Status', 'CreatedDate',))

write_issues(r)

if 'link' in r.headers:
    print r.headers
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    print "***"
    print pages
    while 'last' in pages and 'next' in pages:
        print pages['next']
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        if pages['next'] == pages['last']:
            break
        pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])

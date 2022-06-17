from github import Github

account = Github("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")

repo = account.get_repo("riick-013/SmartLauncher")

print(list(repo.get_branches()))

#contents = repo.get_contents("")
#print(contents)

# Donwnload file form ContenFile object info:
#urllib.urlretrieve(contents.download_url, "name-for-your-file")
Typical steps:

1️⃣ Make sure your latest changes are committed:
```
git add base.config
git commit -m "Add manifest block with version info"
git push origin main  # push your latest commit to main
```

2️⃣ Then create the Git tag (e.g. for version 1.0.0):

`git tag 1.0.0`

3️⃣ Push the tag to GitHub:

`git push origin 1.0.0`


`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git remote rename origin bitbucket`
Renaming remote references: 100% (3/3), done.

`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git remote add origin https://github.com/JD2112/nimbus-dds.git`
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git remote -v`
bitbucket       https://JD2112@bitbucket.org/JD2112/php-sql.git (fetch)
bitbucket       https://JD2112@bitbucket.org/JD2112/php-sql.git (push)
origin  https://github.com/JD2112/nimbus-dds.git (fetch)
origin  https://github.com/JD2112/nimbus-dds.git (push)
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git push origin --all`
Enumerating objects: 246, done.
Counting objects: 100% (246/246), done.
Delta compression using up to 16 threads
Compressing objects: 100% (239/239), done.
Writing objects: 100% (246/246), 13.32 MiB | 12.89 MiB/s, done.
Total 246 (delta 81), reused 3 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (81/81), done.
To https://github.com/JD2112/nimbus-dds.git
 * [new branch]      main -> main
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git push origin --tags`
Everything up-to-date
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git tag 1.0.0`
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git push origin 1.0.0`
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/JD2112/nimbus-dds.git
 * [new tag]         1.0.0 -> 1.0.0
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git describe --tags --abbrev=0`

1.0.0
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git tag -d 1.0.0`
Deleted tag '1.0.0' (was 24713af)
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git push origin :refs/tags/1.0.0`
To https://github.com/JD2112/nimbus-dds.git
 - [deleted]         1.0.0
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git tag v0.1.0`
`jyoda68 ~/Documents/JDCo/Apps-Docs-Plans/weblogin/php-sql [main] $ git push origin v0.1.0`
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/JD2112/nimbus-dds.git
 * [new tag]         v0.1.0 -> v0.1.0


## Git Commit New

`make-templates`
`git add .`
`export GPG_TTY=$(tty)`
`git commit -S -m "git essentials files added"`
`git push`
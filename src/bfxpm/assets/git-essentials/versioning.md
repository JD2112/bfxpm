## GitHub repository versioning

### 1. Initialize Git & push to GitHub

```bash
# in your mkdocs project folder
git init
git add .
git commit -m "Initial commit with MkDocs site"

# create a new GitHub repo online (e.g., my-mkdocs-site)
# then connect local repo to GitHub
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

### 2. Add version number and tag release

```bash
git add .
git commit -S -m "Update docs for v1.1.0"

# Create a version tag
git tag -a v1.1.0 -m "Release v1.1.0"

# Push code + tags to GitHub
git push origin main --tags
```

### 3. Publish to GitHub Pages 
```bash
mkdocs gh-deploy
```

??? warning "Note on mkdocs gh-deploy"
    The `mkdocs gh-deploy` command will push your documentation to the `gh-pages` branch of your repository.
    This is the branch that GitHub Pages uses to serve your site.
    use `mike deploy` instead for versioning.

## GitHub Pages versioning with mike

### 1. Install mike
Run in your local environment:
`pip install mike`

You can check it’s installed with:
`mike --version`

### 2. Update mkdocs.yml
Open your mkdocs.yml and add the mike plugin:

```yml
plugins:
  - search
  - mike

Optionally, you can configure it to set the default version:

```yml
extra:
  version:
    provider: mike
```

### 3. Remove old deployment (optional, cleanup)
Since mkdocs gh-deploy previously wrote files into the gh-pages branch, you can either keep them as a backup or clean them up before switching.
If you want to start fresh:

```bash
git checkout gh-pages
git rm -rf .
git commit -m "cleanup for mike migration"
git push origin gh-pages
git checkout main
```

### 4. First deployment with mike
From your repo root (where mkdocs.yml lives), run:

```bash
# Build and deploy docs as version 1.0, also tag it as "latest"
mike deploy --push --update-aliases 1.0 latest
```

This does:

- Builds your docs
- Writes them under /1.0/ and /latest/ on the gh-pages branch
- Adds/updates the version dropdown

### 5. Set default version
You also need to tell GitHub Pages what version should load when people open your main site URL.
Do:

```bash
mike set-default --push latest
```
Now, visiting https://jd2112.github.io/bioinformatics_courses/ will open latest/.

### 6. Add future versions
When you update the tutorials and want to make a new release (say 1.1):

```bash
mike deploy --push --update-aliases 1.1 latest
mike set-default --push latest
```

That way:

- /1.0/ stays as historical
- /1.1/ gets created
- /latest/ points to 1.1

### 7. Tagging GitHub releases (optional but recommended)
To mirror version numbers in GitHub releases, you can do:

```bash
git tag -a v1.0 -m "Release 1.0 of tutorials"
git push origin v1.0
```

Then your repo will have both:

GitHub release tags (v1.0, v1.1)
Matching documentation versions (/1.0/, /1.1/)

### 8. Verify
After deploying, check:

`https://jd2112.github.io/bioinformatics_courses/latest/`

- Dropdown in top navbar (should say latest, with 1.0 listed)
- Sidebar and all tutorials still working

✅ From now on, you never run mkdocs gh-deploy again.
You always deploy using mike deploy.

??? note "Debugging"
    If you run into "local changes will be overwrittten" issues, check:

   ```bash
    git add mkdocs.yml
    git commit -S -m "Add mike plugin for versioning"
    git push origin main
    git checkout gh-pages

    mike deploy --push --update-aliases 1.0 latest
    mike set-default --push latest
   ```

??? note "tagging releases manually"
    If you want to tag releases manually without using mike, follow these steps:
    # List all tags
    `git tag`

    # Delete old tags locally
    `git tag -d v1.3.0 v1.3.1 v1.3.2 v1.3.3 v1.3.4 v1.3.5 v1.3.6 v1.3.7 v1.3.8 v1.3.9 v1.3.10`

    # Delete old tags on remote
    ```bash
    git push origin :refs/tags/v1.3.0
    git push origin :refs/tags/v1.3.1
    git push origin :refs/tags/v1.3.2
    git push origin :refs/tags/v1.3.3
    git push origin :refs/tags/v1.3.4
    git push origin :refs/tags/v1.3.5
    git push origin :refs/tags/v1.3.6
    git push origin :refs/tags/v1.3.7
    git push origin :refs/tags/v1.3.8
    git push origin :refs/tags/v1.3.9
    git push origin :refs/tags/v1.3.10
    ```
    
    # Create a clean new tag
    `git tag v1.3.0`

    # Push the new tag to GitHub
    `git push origin v1.3.0`


## Pulling and pushing old tags from old repo to new repo
Fetch everything from the old repo, but without updating tags automatically:
git fetch source --no-tags
This fetches branches only (main, v1.1, v1.2, etc.), no tags.
Manually fetch tags one by one, excluding v1.3.0:
git fetch source tag v1.0
git fetch source tag v1.1
git fetch source tag v1.2
git fetch source tag v1.2.1
git fetch source tag v1.2.2
git fetch source tag v1.2.3
git fetch source tag v1.2.4
That way, only those tags are imported. Your local v1.3.0 remains untouched.

3. Verify tags
git tag -l

4. Push branches and tags to the new repo
push all tags:
git push origin --tags
push all branches:
git push origin --all
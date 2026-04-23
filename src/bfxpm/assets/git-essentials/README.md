[![docker-image](https://github.com/JD2112/MyBookLibrary/actions/workflows/docker-build.yml/badge.svg)](https://github.com/JD2112/MyBookLibrary/actions/workflows/docker-build.yml)
![Docker Image Version (tag)](https://img.shields.io/docker/v/jd21/mybooklist/latest?arch=amd64&style=plastic&logo=docker&link=https%3A%2F%2Fhub.docker.com%2Frepository%2Fdocker%2Fjd21%2Fmybooklist%2Fgeneral)
[![wakatime](https://wakatime.com/badge/user/fe95275f-909a-4147-a45d-624981173898/project/018c0128-45e9-45b5-b717-402269aab9a2.svg)](https://wakatime.com/badge/user/fe95275f-909a-4147-a45d-624981173898/project/018c0128-45e9-45b5-b717-402269aab9a2)

![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=JD2112.JD2112)
[![wakatime](https://github.com/JD2112/JD2112/actions/workflows/waka-readme.yml/badge.svg)](https://github.com/JD2112/JD2112/actions/workflows/waka-readme.yml)
[![wakatime](https://wakatime.com/badge/user/fe95275f-909a-4147-a45d-624981173898.svg)](https://wakatime.com/@fe95275f-909a-4147-a45d-624981173898)
[![Website Badge](https://img.shields.io/badge/website-informational?style=flat-square)](http://jyotirmoydas.netlify.app)
[![DOI](https://zenodo.org/badge/668165851.svg)](https://zenodo.org/doi/10.5281/zenodo.11104069)

[![Twitter Follow](https://img.shields.io/twitter/follow/jyotirmoy21?style=social)](https://twitter.com/jyotirmoy21)
[![Linkedin Badge](https://img.shields.io/badge/-jyotirmoy-blue?style=plastic&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/dasjyotirmoy/)](https://www.linkedin.com/in/dasjyotirmoy/)
[![Google Scholar Badge](https://img.shields.io/badge/-jyotirmoy-blue?style=plastic&logo=GoogleScholar&logoColor=white&link=https://scholar.google.se/citations?user=IMBYOv8AAAAJ&hl=en)](https://scholar.google.se/citations?user=IMBYOv8AAAAJ&hl=en)
[![ResearchGate Badge](https://img.shields.io/badge/-jyotirmoy-cyan?style=plastic&logo=ResearchGate&logoColor=white&link=https://www.researchgate.net/profile/Jyotirmoy-Das-3)](https://www.researchgate.net/profile/Jyotirmoy-Das-3)
[![ORCiD Badge](https://img.shields.io/badge/-jyotirmoy-green?style=plastic&logo=orcid&logoColor=white&link=https://orcid.org/0000-0002-5649-4658)](https://orcid.org/0000-0002-5649-4658)
[![Loop Badge](https://img.shields.io/badge/-jyotirmoy-orange?style=plastic&logo=Loop&logoColor=white&link=https://loop.frontiersin.org/people/1519976/overview)](https://loop.frontiersin.org/people/1519976/overview)

[![trophy](https://github-profile-trophy.vercel.app/?username=JD2112)](https://github.com/ryo-ma/github-profile-trophy)

[![Netlify Status](https://api.netlify.com/api/v1/badges/441b744c-9200-4c1b-8bf9-5d82f2bba7db/deploy-status)](https://app.netlify.com/sites/core-facility-bioinformatics/deploys)
[![pages-build-deployment](https://github.com/JD2112/CF-manual/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/JD2112/CF-manual/actions/workflows/pages/pages-build-deployment)
[![Netlify Status](https://api.netlify.com/api/v1/badges/c418a8d2-9869-4489-a253-1aa3f1364756/deploy-status)](https://app.netlify.com/sites/jbioinformatics-core-facility/deploys)

[![methylr-registration-form](https://github.com/JD2112/methylr-registration-form/actions/workflows/main.yaml/badge.svg)](https://github.com/JD2112/methylr-registration-form/actions/workflows/main.yaml)

[![docker-image](https://github.com/JD2112/jyotirmoy-website/actions/workflows/docker-build.yml/badge.svg)](https://github.com/JD2112/jyotirmoy-website/actions/workflows/docker-build.yml)
[![Deploy static content to Pages](https://github.com/JD2112/jyotirmoy-website/actions/workflows/github-pages.yml/badge.svg)](https://github.com/JD2112/jyotirmoy-website/actions/workflows/github-pages.yml)
[![wakatime](https://wakatime.com/badge/user/fe95275f-909a-4147-a45d-624981173898/project/2b09acf7-8ea5-4e7f-9d13-9af65fec8c4a.svg)](https://wakatime.com/badge/user/fe95275f-909a-4147-a45d-624981173898/project/2b09acf7-8ea5-4e7f-9d13-9af65fec8c4a)

## Quarto render

`quarto render --profile production && quarto render --profile advanced`

## Password protection

```{r echo=FALSE, eval=FALSE}
library(fidelius)
charm("docs/index.html", password = "Bvd^Z5.Wqil^j", hint = "A very bad password!")
charm("_docs-advanced/index.html", password = "Jyotirmoy@document", hint = "A very bad password!")
```




## Docker Memory Monitor from terminal
To monitor memory usage for a single container by its container ID, modify the script as follows:

```bash
#!/bin/bash

# Usage: ./docker_mem_monitor.sh <container_id>
CONTAINER_ID="$1"
OUTFILE="docker_mem_usage_${CONTAINER_ID}.csv"

if [ -z "$CONTAINER_ID" ]; then
    echo "Usage: $0 <container_id>"
    exit 1
fi

# Write header
echo "timestamp,container_id,container_name,memory_usage,memory_limit,percent" > "$OUTFILE"

# Loop for 10 minutes (120 samples, 5s each)
for i in {1..120}; do
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    stats=$(docker stats --no-stream --format "{{.ID}},{{.Name}},{{.MemUsage}},{{.MemPerc}}" "$CONTAINER_ID")
    IFS=',' read -r id name memusage memperc <<< "$stats"
    usage=$(echo "$memusage" | awk -F' / ' '{print $1}')
    limit=$(echo "$memusage" | awk -F' / ' '{print $2}')
    echo "$timestamp,$id,$name,$usage,$limit,$memperc" >> "$OUTFILE"
    sleep 5
done
```

**Usage:**
```bash
chmod +x docker_mem_monitor.sh
./docker_mem_monitor.sh <container_id>
```
This will create a CSV file with memory stats for the specified container only.
```bash
#!/bin/bash

# Output file
OUTFILE="docker_mem_usage.csv"

# Write header
echo "timestamp,container_name,memory_usage,memory_limit,percent" > "$OUTFILE"

# Loop for 10 minutes (120 samples, 5s each)
for i in {1..120}; do
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Get stats for all containers
    docker stats --no-stream --format "{{.Name}},{{.MemUsage}},{{.MemPerc}}" | while IFS=',' read -r name memusage memperc; do
        # Split "123MiB / 2GiB" into usage and limit
        usage=$(echo "$memusage" | awk -F' / ' '{print $1}')
        limit=$(echo "$memusage" | awk -F' / ' '{print $2}')
        
        echo "$timestamp,$name,$usage,$limit,$memperc" >> "$OUTFILE"
    done

    sleep 5
done

```

1. Save the script to a file, e.g., `docker_mem_monitor.sh`.
2. Make it executable:
   ```bash
   chmod +x docker_mem_monitor.sh
   ```
3. Run the script:
   ```bash
   ./docker_mem_monitor.sh
   ```
This will create a CSV file named `docker_mem_usage.csv` with the memory usage statistics of all running Docker containers every 5 seconds for 10 minutes.

## Notes in markdown. - 
Here’s a list of the most common ones you can swap in:
note → 💡 informational note
info → ℹ️ general information
tip / hint → ✅ helpful suggestion or best practice
important → ⭐️ important highlight
warning / caution → ⚠️ warnings, things to be careful about
danger → 🚨 critical danger, severe risks
success → 🎉 success message
failure / error / bug → ❌ issues, errors, or bugs
abstract / summary → 📄 summaries or key takeaways
question / help → ❓ FAQs, guidance


Perfect — here’s a single-line, workflow-safe command sequence you can run from your local pac-cpg branch. It will:
Stage all changes
Commit them
Push to your fork only (origin)
Skip GitHub Actions/workflows
`git add . && git commit -m "Update pac-cpg branch [skip ci]" && git push origin pac-cpg`
✅ What this does:
`git add .` → stages all modified files
`git commit -m "… [skip ci]"` → commits changes locally without triggering workflows
`git push origin pac-cpg` → pushes to your fork branch only, leaving upstream untouched

## Move a branch from public to private repo

```bash
#!/usr/bin/env bash

set -e  # exit if any command fails

OLD_REMOTE="origin"
NEW_REMOTE="private"
NEW_REPO_URL="https://github.com/JD2112/jd2112-website.git"
BRANCH="website"

echo "🔍 Checking that branch '$BRANCH' exists locally..."
git rev-parse --verify "$BRANCH" >/dev/null

echo "➡️ Switching to branch '$BRANCH'..."
git checkout "$BRANCH"

echo "➕ Adding new private repo as remote '$NEW_REMOTE'..."
git remote add "$NEW_REMOTE" "$NEW_REPO_URL"

echo "🚀 Pushing branch '$BRANCH' to private repo..."
# Push it as 'main' in the new repo (recommended), OR:
git push "$NEW_REMOTE" "$BRANCH:main"

# If you prefer the same branch name in the new repo:
# git push "$NEW_REMOTE" "$BRANCH:$BRANCH"

echo "🧹 Deleting branch '$BRANCH' from public repo ($OLD_REMOTE)..."
git push "$OLD_REMOTE" --delete "$BRANCH"

echo "✔️ Transfer complete!"
echo "📌 '$BRANCH' now lives in: $NEW_REPO_URL"
echo "📌 And it has been removed from the public repo."

```
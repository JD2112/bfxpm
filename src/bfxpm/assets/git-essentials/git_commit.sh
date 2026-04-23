```
git init
git branch -M main
git add .
git commit -m "first commit"
git remote add origin https://github.com/JD2112/RNAseq_Analysis.git
git remote -v
git push -u origin main

#A. Custom Tag at Your message
#Put [Skip ci] or [ci Skip] in your commit message.

git commit -m “Your fancy message [skip ci]” or git commit -m “Your fancy message [ci skip]
#B. Using Git push options
#In this scenario, you can skip ci execution for a specific commit push
git push origin <branch> --push-option=ci.skip or git push -o ci.skip 


```


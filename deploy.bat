@echo off

rem Add changes, commit, and push
git add .
git commit -m "merge for deployment"
git push

rem Switch to the main branch, reset to the desired commit, and force-push
git checkout main
git reset --hard web50/projects/2020/x/capstone
git push --force myrepo main

rem Switch back to the capstone branch
git checkout web50/projects/2020/x/capstone

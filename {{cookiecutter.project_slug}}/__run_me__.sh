#!/usr/bin/env bash
name={{ cookiecutter.github_repo_name }}
vis={{ cookiecutter.github_visability }}
cd $(dirname $0)
git init
uv add bump2version
uv lock
git add .
git commit -m "first commit"
gh repo create ${name} ${vis}
git remote add origin git@github.com:bryanhann/${name}.git
git branch -M main
git push -u origin main
uv run ./my.bump patch && {
    mkdir .hide
    mv $(basename $0) .hide
}

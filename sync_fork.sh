#!/bin/bash

# Sincroniza el fork con el upstream. Borra todos los cambios locales y los del fork.
# sync_fork.sh
git fetch upstream
git checkout master
git reset --hard upstream/master
git push origin master --force
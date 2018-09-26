#!/bin/sh

cd $(dirname "$0") || exit 1
find . -name "*.pyc" -type d -delete
rm -rf .tmp/* last_run/* test_run/*
git add .
git commit -m "$1"
git push -u origin master

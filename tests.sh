#!/bin/sh
find . ! -name "$(printf "*\n*")" -name '*.py' > tmp
while IFS= read -r file; do
  printf "Running flake8 on %s.... Result: " "$file"
  flake8 --count "$file"
done < tmp
rm tmp

find . ! -name "$(printf "*\n*")" -name '*.sh' > tmp
while IFS= read -r file; do
  printf "Running shellcheck on %s.... Result: " "$file"
  shellcheck "$file"
  echo "$?"
done < tmp
rm tmp

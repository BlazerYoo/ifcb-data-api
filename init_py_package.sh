echo 'Initializing Python package environment...'

package_name=$1
author=$2
email=$3
description=$4
cli_name=$5

# Create directory structure
mkdir package_directory
cd package_directory
#mkdir src
#cd src
mkdir $package_name
cd $package_name
touch __init__.py
touch "$package_name.py"

# Create directory structure + toml: [build-system]
cd ..
echo $'[build-system]\nrequires = ["setuptools"]\nbuild-backend = "setuptools.build_meta"' > pyproject.toml
mkdir tests

# toml: [project]
echo $'\n[project]' >> pyproject.toml
printf "%s" "name = \"$package_name\"" >> pyproject.toml
echo $'\nversion = "0.0.1"' >> pyproject.toml
printf "%s" "authors = [{ name=\"$author\", email=\"$email\" },]" >> pyproject.toml
echo >> pyproject.toml
printf "%s" "description = \"$description\"" >> pyproject.toml
echo $'\nreadme = "README.md"' >> pyproject.toml
echo $'requires-python = ">=3.7"' >> pyproject.toml
echo $'classifiers = [' >> pyproject.toml
cat ../classifiers.txt >> pyproject.toml
echo $'\n]'   >> pyproject.toml

echo $'dependencies = [' >> pyproject.toml
cat ../dependencies.txt >> pyproject.toml
echo $'\n]'   >> pyproject.toml

# toml: [project.urls]
echo $'\n[project.urls]' >> pyproject.toml
printf "%s" "\"Homepage\" = \"https://github.com/$author/$package_name\"" >> pyproject.toml
echo >> pyproject.toml
printf "%s" "\"Bug Tracker\" = \"https://github.com/$author/$package_name/issues\"" >> pyproject.toml

# toml: [project.scripts]
echo $'\n\n[project.scripts]' >> pyproject.toml
printf "%s" "$cli_name = \"$package_name.$package_name:main\"" >> pyproject.toml

# README.md
echo "# $package_name" > README.md
echo >> README.md
echo "$description" >> README.md

# LICENSE
cat ../license.txt > LICENSE

# Prompt edit of __main__.py
read  -n 1 -p "Edit $package_name.py then come back and press [ENTER] to continue" mainmenuinput

# Build
#python -m build

# Upload
#twine upload --repository testpypi dist/*

# Prompt exit
read  -n 1 -p 'Press [ENTER] to terminate' mainmenuinput
exit 0
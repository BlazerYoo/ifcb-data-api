# Upgrade pip
pip install --upgrade pip

echo 'Initializing Python package environment...'

package_name=$1
author=$2
email=$3
description=$4

# Create directory structure
mkdir package_directory
cd package_directory
mkdir src
cd src
mkdir $package_name
cd $package_name
touch __init__.py
touch "$package_name.py"

# Create directory structure + toml: [build-system]
cd ..
cd ..
touch LICENSE
echo $'[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"' > pyproject.toml
touch README.md
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
printf "%s" "classifiers = [\"Programming Language :: Python :: 3\", \"License :: OSI Approved :: GNU Affero General Public License v3\", \"Operating System :: OS Independent\",]" >> pyproject.toml

# toml: [project.urls]
echo $'\n\n[project.urls]' >> pyproject.toml
printf "%s" "\"Homepage\" = \"https://github.com/$author/$package_name\"" >> pyproject.toml
echo >> pyproject.toml
printf "%s" "\"Bug Tracker\" = \"https://github.com/$author/$package_name/issues\"" >> pyproject.toml

# README.md
echo "# $package_name" > README.md
echo >> README.md
echo "$description" >> README.md

# LICENSE
cat ../license.txt > LICENSE

# Install/upgrade build
pip install --upgrade build

# Run build

# Prompt exit
read  -n 1 -p 'Press [ENTER] to terminate' mainmenuinput
exit 0
This is a file browser front-end for dataset upload server.

# Develop

## Prepare Env
```
pipenv --python 3.6.8 (or other compatible versions)
pipenv shell
pipenv install
cd app/static
npm install
```

## Install New Python Package
```
pipenv shell
pipenv install <package name>
```

# Build Docker Image
```
pipenv shell
pipenv lock -r > requirements.txt
./build.sh
```
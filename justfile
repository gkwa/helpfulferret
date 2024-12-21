set shell := ["bash", "-uec"]

shell_files := `find . \( -name .git -o -name node_modules -o -name .venv -o -name .ruff_cache \) -prune -o -name "*.sh" -print | tr '\n' ' ' `
py_files := `find . \( -name .git -o -name node_modules -o -name .venv -o -name .ruff_cache \) -prune -o -name "*.py" -print | tr '\n' ' ' `
bucket := 'streambox-helpfulferret'

[group('maint')]
default:
    @just --list

[group('setup')]
run:
    #!/usr/bin/env bash
    . .venv/bin/activate
    python -m spacy download en_core_web_sm
    helpfulferret categorize -v -v
    helpfulferret show

[group('setup')]
setup:
    #!/usr/bin/env bash
    apt-get update
    apt-get install -y wamerican
    uv sync
    . .venv/bin/activate
    python -m spacy download en_core_web_sm
    python main.py

[group('maint')]
pre-commit:
    pre-commit sample-config >.pre-commit-config.yaml
    pre-commit install --config .pre-commit-config.yaml
    git add .pre-commit-config.yaml
    pre-commit run --all-files

[group('maint')]
fmt:
    test -z "{{ py_files }}" || { ruff format .; ruff check --fix; }
    test -z "{{ shell_files }}" || shfmt -w -s -i 4 {{ shell_files }}
    terraform fmt -recursive .
    prettier --ignore-path=.prettierignore --config=.prettierrc.json --write .
    just --unstable --fmt

[group('lint')]
lint:
    test -z "{{ shell_files }}" || shellcheck {{ shell_files }}

[group('setup')]
bucket-setup:
    terraform init
    terraform plan -out=tfplan -var="{{ bucket }}"
    terraform apply tfplan

[group('bucket')]
fetch-data:
    #!/usr/bin/env bash
    mkdir -p txt-files
    aws s3 cp s3://streambox-helpfulferret/txt-files.tar.zip txt-files
    unzip txt-files/txt-files.tar.zip -d txt-files
    tar -xvf txt-files/txt-files.tar -C txt-files
    find txt-files/cache/epub/ -name "*.txt"

[group('bucket')]
ls:
    aws s3 ls s3://streambox-helpfulferret --recursive

[group('bucket')]
put:
    aws s3 cp txt-files.tar.zip s3://streambox-helpfulferret/

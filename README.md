# Makefile Pretty Help Script

Basic python script that makes it easy to print pretty help text for your Makefile.

## Installation

    wget 'https://github.com/jweede/makefile-pretty-help-script/raw/master/makefile_self_document.py'
    chmod +x makefile_self_document.py

## Usage

Drop into your project, make a new make target like:

    ##> help : Show this help text
    .PHONY: help
    help:
    	@python scripts/makefile_self_document.py $(MAKEFILE_LIST)

This script scans the makefiles for:

 - Section headers: `#### Install Section ####`
 - Target descriptions: `target/cmd: ## Builds the cmd`
 - `.PHONY` targets: `.PHONY: install ## Installs things`
 
 and generates help text that looks like:
 
```text
>> Generic Makefile <<

make                         default target is help
make help                    this help text
make clean                   removes artifacts
make install                 installs global executables
make build                   builds dev environment

>> Documentation <<

make docs                    generate documentation
make docs-publish            publish documentation
make docs-watch              launch a live-updating local docs server

>> Testing <<

make test                    run tests

```

## Self-update

    ./makefile_self_document.py --update

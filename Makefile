# Makefile
# aws-cdk-static-site
#
# Copyright © 2026 Dagitali LLC. All rights reserved.
#
# Facilitates automation for local development environments.
#
# Responsibilities
# - Automate common local setup, quality, testing, and packaging workflows.
# - Provide stable, discoverable entry points shared by contributors and CI.
#
# Maintainer Notes
# - Keep common target names and help text consistent with other Dagitali
#   projects when their behavior is equivalent.
# - Keep project-specific commands and variables clearly labeled so reusable
#   conventions can be extracted without coupling projects.
# - Prefer overridable variables for paths, interpreters, and outputs.
#
# References
# - GNU Make documentation:
#   https://www.gnu.org/software/make/manual/make.html
# - GNU Make conventions:
#   https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html
# - GNU Make include directive:
#   https://www.gnu.org/software/make/manual/html_node/Include.html
#
# Common Flows
#
# 1) Create the development environment.
# $ make dev
#
# 2) Run the local CI-equivalent checks.
# $ make check
#
# 3) Run the default test suite.
# $ make test
#
# 4) Build the local documentation with CI-equivalent validation.
# $ make docs-strict
#
# 5) Inspect the local environment.
# $ make show-venv
#
# 6) Clean build artifacts or nuke the venv.
# $ make clean
# $ make clean-venv


# SECTION: VARIABLES

SHELL := /bin/bash

### Environment ###

# Load conventional local overrides when present. Override ENV_FILE with an
# empty value to disable loading or with another Make-compatible env file.
ENV_FILE ?= .env
ifneq ($(strip $(ENV_FILE)),)
-include $(ENV_FILE)
endif

### Make ###

.DEFAULT_GOAL := help
HELP_TARGET_WIDTH ?= 20
SHARED_MAKEFILE ?=

### Project ###

PROJECT_NAME ?= $(notdir $(CURDIR))
EXAMPLES_DIR ?= examples
SCRIPTS_DIR ?= scripts
SOURCE_DIR ?= src
TESTS_DIR ?= tests

PYTHON_POLICY_SCRIPT ?= $(SCRIPTS_DIR)/check_python_policy.py
RELEASE_CHANGELOG_SCRIPT ?= $(SCRIPTS_DIR)/check_release_changelog.py
WORKFLOW_PINS_SCRIPT ?= $(SCRIPTS_DIR)/check_workflow_pins.py

RELEASE_VERSION ?=

PACKAGE_FORMAT ?= tar.gz
PACKAGE_OUTPUT ?= $(subst .,-,$(PROJECT_NAME))-repository.$(PACKAGE_FORMAT)
PACKAGE_PREFIX ?= $(PROJECT_NAME)/

### Cleanup ###

CLEAN_SEARCH_DIRS ?= $(SOURCE_DIR) $(TESTS_DIR) $(SCRIPTS_DIR) $(EXAMPLES_DIR)
CLEAN_REMOVE_PATHS ?= build .coverage coverage.xml htmlcov $(DOCS_BUILD_DIR) \
	.mypy_cache .pytest_cache .ruff_cache $(PKG_DIR)/*.egg-info \
	$(SOURCE_DIR)/*.egg-info

### Documentation ###

DOCS_SOURCE_DIR ?= docs/source
DOCS_BUILD_DIR ?= docs/build
SPHINX_STRICT_FLAGS ?= -T -W --keep-going

### Installation ###

VENV_READY_COMMAND ?= true
RUNTIME_INSTALL_COMMAND ?= $(PIP) install $(PIP_INSTALL_FLAGS) $(RUNTIME_INSTALL_ARGS)
DEV_INSTALL_COMMAND ?= $(PIP) install $(PIP_INSTALL_FLAGS) $(DEV_INSTALL_ARGS)
DOCS_INSTALL_COMMAND ?= $(PIP) install $(PIP_INSTALL_FLAGS) $(DOCS_INSTALL_ARGS)
RUNTIME_POST_INSTALL_COMMAND ?= true
DEV_POST_INSTALL_COMMAND ?= $(RUNTIME_POST_INSTALL_COMMAND)

HOOK_INSTALL_ARGS ?= --install-hooks

### Python ###

# Python to bootstrap the venv. To override the interpreter, set PY on the CLI:
#   make dev PY=python3.13
#   make dev PY=python3.14
PY ?= python3
MINIMUM_PYTHON_VERSION ?= 3.13
MAXIMUM_PYTHON_VERSION ?= 3.15

# Package root (where pyproject.toml lives)
PKG_DIR ?= .
PYTHON_DIST_DIR ?= $(PKG_DIR)/dist

# Virtualenv lives inside the package folder
VENV_DIR ?= $(PKG_DIR)/.venv

# Cross-platform venv bin paths
ifeq ($(OS),Windows_NT)
VENV_BIN := $(abspath $(VENV_DIR)/Scripts)
PYTHON ?= $(VENV_BIN)/python.exe
else
VENV_BIN := $(abspath $(VENV_DIR)/bin)
PYTHON ?= $(VENV_BIN)/python
endif

MYPY ?= $(PYTHON) -m mypy
PIP ?= $(PYTHON) -m pip
PRE_COMMIT ?= $(PYTHON) -m pre_commit
PYTEST ?= $(PYTHON) -m pytest
RUFF ?= $(PYTHON) -m ruff
PYTHON_BUILD ?= $(PYTHON) -m build
SPHINX ?= $(PYTHON) -m sphinx
TWINE ?= $(PYTHON) -m twine

PIP_INSTALL_FLAGS ?= --disable-pip-version-check
RUNTIME_INSTALL_ARGS ?= -e "$(abspath $(PKG_DIR))"
DEV_INSTALL_ARGS ?= -e "$(abspath $(PKG_DIR))[dev]"
DOCS_INSTALL_ARGS ?= -e "$(abspath $(PKG_DIR))[docs]"

PYTHON_FORMAT_PATHS ?= .
PYTHON_LINT_PATHS ?= $(PYTHON_FORMAT_PATHS)
PYTHON_TYPECHECK_PATHS ?= $(SOURCE_DIR) $(TESTS_DIR) $(SCRIPTS_DIR)

### Packaging (Git) ###

PACKAGE_BUILD_COMMAND ?= git archive --format=$(PACKAGE_FORMAT) \
	--prefix="$(PACKAGE_PREFIX)" --output="$(PACKAGE_OUTPUT)" HEAD

### Packaging (Python) ###

DIST_BUILD_COMMAND ?= $(PYTHON_BUILD) --outdir "$(PYTHON_DIST_DIR)"
DIST_CHECK_COMMAND ?= $(TWINE) check "$(PYTHON_DIST_DIR)"/*

### Quality ###

BASE_CHECK_TARGETS ?= python-policy lint typecheck workflow-pins test
CHECK_TARGETS ?= $(BASE_CHECK_TARGETS) dist
CHECK_PRE_PUSH_TARGETS ?= $(BASE_CHECK_TARGETS)
CHECK_CI_LOCAL_TARGETS ?= $(CHECK_TARGETS) docs-strict
CI_SMOKE_TARGETS ?= python-policy lint test-unit

### Testing ###

TEST_PYTHONPATH ?= $(abspath $(SOURCE_DIR))
TEST_ENV ?= PYTHONPATH="$(TEST_PYTHONPATH)"
PYTEST_COMMON_ARGS ?=
TEST_MARK_EXPRESSION ?=
PYTEST_MARK_ARGS = $(if $(strip $(TEST_MARK_EXPRESSION)),\
	-m "$(TEST_MARK_EXPRESSION)")
TEST_ARGS ?= $(PYTEST_COMMON_ARGS) $(PYTEST_MARK_ARGS)

FULL_TEST_TARGETS ?= test

UNIT_TEST_PATH ?= $(TESTS_DIR)/unit
UNIT_TEST_ARGS ?= $(PYTEST_COMMON_ARGS) $(PYTEST_MARK_ARGS) $(UNIT_TEST_PATH)

INTEGRATION_TEST_PATH ?= $(TESTS_DIR)/integration
INTEGRATION_TEST_ARGS ?= $(PYTEST_COMMON_ARGS) $(PYTEST_MARK_ARGS) \
	--no-cov $(INTEGRATION_TEST_PATH)

# !SECTION

# SECTION: MACROS

define ASSERT_REPOSITORY_PATH
	case "$(abspath $(1))" in \
		"$(CURDIR)"/*) ;; \
		*) echo "$(2) must be inside $(CURDIR)" >&2; exit 1 ;; \
	esac
endef

define ASSERT_REPOSITORY_SEARCH_PATH
	case "$(abspath $(1))" in \
		"$(CURDIR)"|"$(CURDIR)"/*) ;; \
		*) echo "$(2) must be $(CURDIR) or one of its children" >&2; exit 1 ;; \
	esac
endef

define ECHO_INFO
	printf "\033[36mℹ\033[0m %s\n" "$(1)"
endef

define ECHO_OK
	printf "\033[32m✔\033[0m %s\n" "$(1)"
endef

define RUN_IN_PACKAGE
	cd "$(PKG_DIR)" && $(1)
endef

define RUN_SPHINX_BUILD
	$(DOCS_INSTALL_COMMAND)
	@rm -rf "$(DOCS_BUILD_DIR)/$(1)" "$(DOCS_BUILD_DIR)/doctrees/$(1)"
	$(SPHINX) $(2) -b $(1) -d "$(DOCS_BUILD_DIR)/doctrees/$(1)" \
		"$(DOCS_SOURCE_DIR)" "$(DOCS_BUILD_DIR)/$(1)"
	@$(call ECHO_OK,Built $(1) documentation in $(DOCS_BUILD_DIR)/$(1))
endef

# !SECTION

# Optionally load versioned common rules from a local path, such as a Make
# fragment installed by a development-tooling package. Project values above
# are available to the shared rules, and local targets below remain explicit.
ifneq ($(strip $(SHARED_MAKEFILE)),)
include $(SHARED_MAKEFILE)
endif

# SECTION: PHONY TARGETS

##@ Utilities

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS=":.*##"; printf "\nUsage: make \033[36m<TARGET>\033[0m\n\nTargets:\n"} \
	/^[a-zA-Z0-9_-]+:.*##/ {printf "  \033[36m%-*s\033[0m %s\n", $(HELP_TARGET_WIDTH), $$1, $$2} \
	/^##@/ {printf "\n\033[1m%s\033[0m\n", substr($$0, 5)}' $(MAKEFILE_LIST)

.PHONY: check-python-runtime
check-python-runtime: ## Require a supported Python version for local project commands
	@$(PY) -c \
		'import sys; minimum=tuple(map(int, "$(MINIMUM_PYTHON_VERSION)".split("."))); maximum=tuple(map(int, "$(MAXIMUM_PYTHON_VERSION)".split("."))); current=sys.version_info[:2]; raise SystemExit(0 if minimum <= current < maximum else "Python >=$(MINIMUM_PYTHON_VERSION),<$(MAXIMUM_PYTHON_VERSION) is required")'

.PHONY: venv
venv: check-python-runtime ## Create the Python virtual environment
	@$(call ASSERT_REPOSITORY_PATH,$(VENV_DIR),VENV_DIR)
	@if [ ! -x "$(PYTHON)" ]; then \
		$(call ECHO_INFO,Creating $(VENV_DIR) with $(PY)); \
		$(PY) -m venv "$(VENV_DIR)"; \
	else \
		current="$$($(PYTHON) -V 2>/dev/null || true)"; \
		current="$${current#Python }"; current="$${current%.*}"; \
		requested="$$($(PY) -V)"; \
		requested="$${requested#Python }"; requested="$${requested%.*}"; \
		if [ "$$current" != "$$requested" ]; then \
			$(call ECHO_INFO,Recreating $(VENV_DIR) for Python $$requested; found $$current); \
			rm -rf "$(VENV_DIR)"; \
			$(PY) -m venv "$(VENV_DIR)"; \
		else \
			$(call ECHO_INFO,Using existing environment: $(VENV_DIR)); \
		fi; \
	fi
	@$(VENV_READY_COMMAND)
	@$(call ECHO_OK,Virtual environment ready)

.PHONY: install
install: venv ## Install runtime dependencies
	$(RUNTIME_INSTALL_COMMAND)
	@$(RUNTIME_POST_INSTALL_COMMAND)
	@$(call ECHO_OK,Installed runtime dependencies)

.PHONY: dev
dev: venv ## Install development dependencies
	$(DEV_INSTALL_COMMAND)
	@$(DEV_POST_INSTALL_COMMAND)
	@$(call ECHO_OK,Installed development dependencies)

.PHONY: hooks
hooks: dev ## Install pre-commit hooks
	$(PRE_COMMIT) install $(HOOK_INSTALL_ARGS)
	@$(call ECHO_OK,Installed pre-commit hooks)

.PHONY: setup
setup: dev ## Install the development environment (compatibility alias)

.PHONY: show-venv
show-venv: ## Print virtual-environment and interpreter locations
	@echo "PKG_DIR  = $(PKG_DIR)"
	@echo "VENV_BIN = $(VENV_BIN)"
	@echo "VENV_DIR = $(VENV_DIR)"
	@echo "PY       = $(PY)"
	@echo "PYTHON   = $(PYTHON)"
	@echo "PIP      = $(PIP)"

.PHONY: clean
clean: ## Remove generated build artifacts and caches
	@$(call ASSERT_REPOSITORY_PATH,$(VENV_DIR),VENV_DIR)
	@$(call ASSERT_REPOSITORY_PATH,$(PYTHON_DIST_DIR),PYTHON_DIST_DIR)
	@$(foreach path,$(CLEAN_REMOVE_PATHS),\
		$(call ASSERT_REPOSITORY_PATH,$(path),CLEAN_REMOVE_PATHS);)
	@$(foreach path,$(CLEAN_SEARCH_DIRS),\
		$(call ASSERT_REPOSITORY_SEARCH_PATH,$(path),CLEAN_SEARCH_DIRS);)
	@find $(CLEAN_SEARCH_DIRS) -type d \
		\( -name '__pycache__' -o -name '.mypy_cache' \
		-o -name '.pytest_cache' -o -name '.ruff_cache' \) \
		-prune -exec rm -rf {} + 2>/dev/null || true
	@rm -rf $(CLEAN_REMOVE_PATHS) "$(PYTHON_DIST_DIR)"
	@$(call ECHO_OK,Removed generated artifacts and caches)

.PHONY: clean-venv
clean-venv: ## Remove the Python virtual environment
	@$(call ASSERT_REPOSITORY_PATH,$(VENV_DIR),VENV_DIR)
	@rm -rf "$(VENV_DIR)"
	@$(call ECHO_OK,Removed virtual environment)


##@ Quality

.PHONY: check
check: $(CHECK_TARGETS) ## Run local CI checks

.PHONY: check-pre-push
check-pre-push: $(CHECK_PRE_PUSH_TARGETS) ## Run the local pre-push checks

.PHONY: check-ci-local
check-ci-local: $(CHECK_CI_LOCAL_TARGETS) ## Run the CI-equivalent local checks

.PHONY: fix
fix: python-policy ## Apply safe Ruff fixes to Python code
	$(call RUN_IN_PACKAGE,$(RUFF) check --fix $(PYTHON_LINT_PATHS))

.PHONY: fmt
fmt: fix ## Format Python code with Ruff
	$(call RUN_IN_PACKAGE,$(RUFF) format $(PYTHON_FORMAT_PATHS))

.PHONY: format
format: fmt ## Format Python code (compatibility alias)

.PHONY: lint
lint: python-policy ## Run Python lint checks
	$(call RUN_IN_PACKAGE,$(RUFF) check $(PYTHON_LINT_PATHS))

.PHONY: typecheck
typecheck: python-policy ## Check Python types
	$(call RUN_IN_PACKAGE,$(MYPY) $(PYTHON_TYPECHECK_PATHS))

.PHONY: workflow-pins
workflow-pins: python-policy ## Verify remote GitHub Actions use immutable commits
	$(PYTHON) $(WORKFLOW_PINS_SCRIPT)

.PHONY: python-policy
python-policy: ## Verify the repository-wide supported Python version policy
	$(PYTHON) $(PYTHON_POLICY_SCRIPT)

.PHONY: release-changelog
release-changelog: ## Verify a dated changelog section (RELEASE_VERSION=x.y.z)
	@test -n "$(strip $(RELEASE_VERSION))" || \
		(echo "RELEASE_VERSION is required" >&2; exit 2)
	$(PY) $(RELEASE_CHANGELOG_SCRIPT) "$(RELEASE_VERSION)"


##@ Testing

.PHONY: test
test: python-policy ## Run the default test suite
	$(call RUN_IN_PACKAGE,$(TEST_ENV) $(PYTEST) $(TEST_ARGS))

.PHONY: test-unit
test-unit: python-policy ## Run isolated unit tests
	$(call RUN_IN_PACKAGE,$(TEST_ENV) $(PYTEST) $(UNIT_TEST_ARGS))

.PHONY: test-integration
test-integration: python-policy ## Run package and example integration tests
	$(call RUN_IN_PACKAGE,$(TEST_ENV) $(PYTEST) $(INTEGRATION_TEST_ARGS))

.PHONY: test-full
test-full: $(FULL_TEST_TARGETS) ## Run all available test suites


##@ Documentation

.PHONY: docs
docs: venv ## Build HTML documentation with Sphinx
	$(call RUN_SPHINX_BUILD,html,)

.PHONY: docs-strict
docs-strict: venv ## Build HTML documentation with CI-parity warning checks
	$(call RUN_SPHINX_BUILD,html,$(SPHINX_STRICT_FLAGS))

.PHONY: docs-epub
docs-epub: venv ## Build EPUB documentation with CI-parity warning checks
	$(call RUN_SPHINX_BUILD,epub,$(SPHINX_STRICT_FLAGS))

.PHONY: docs-linkcheck
docs-linkcheck: venv ## Check documentation links with CI-parity warning checks
	$(call RUN_SPHINX_BUILD,linkcheck,$(SPHINX_STRICT_FLAGS))


##@ CI

.PHONY: ci-smoke
ci-smoke: $(CI_SMOKE_TARGETS) ## Run the fast CI smoke checks


##@ Packaging

.PHONY: dist
dist: python-policy ## Build and validate Python distributions
	@$(call ASSERT_REPOSITORY_PATH,$(PYTHON_DIST_DIR),PYTHON_DIST_DIR)
	@rm -rf "$(PYTHON_DIST_DIR)"
	$(DIST_BUILD_COMMAND)
	$(DIST_CHECK_COMMAND)
	@$(call ECHO_OK,Built Python distributions in $(PYTHON_DIST_DIR))

.PHONY: build
build: dist ## Build Python distributions (compatibility alias)

.PHONY: package
package: python-policy ## Build a repository archive from the current commit
	$(PACKAGE_BUILD_COMMAND)
	@$(call ECHO_OK,Built repository archive: $(PACKAGE_OUTPUT))

# !SECTION

# Makefile for project initialization

# Usage:
#   make project AUTHOR="Your Name" DIR="project_name" [GIT=yes]

AUTHOR ?= Unknown Author
DIR ?= my_project
DATE := $(shell date +%Y-%m-%d)

# Define folder structure
FOLDERS = \
	$(DIR)/scripts \
	$(DIR)/data/meta \
	$(DIR)/data/raw_external \
	$(DIR)/data/raw_internal \
	$(DIR)/doc \
	$(DIR)/intermediate \
	$(DIR)/logs \
	$(DIR)/notebooks \
	$(DIR)/results/figures \
	$(DIR)/results/reports \
	$(DIR)/results/tables \
	$(DIR)/scratch

project:
	@if [ -d "$(DIR)" ]; then \
		echo "$(DIR) already exists."; \
		read -p "Overwrite? (yes/no): " ans; \
		if [ "$$ans" = "yes" ]; then rm -rf "$(DIR)"; echo "Removed existing directory."; \
		else echo "Aborted."; exit 1; fi \
	fi
	@mkdir -p $(FOLDERS)
	@touch $(DIR)/logs/logs.qmd
	@echo "This README file was generated on $(DATE) by $(AUTHOR)" > $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "### GENERAL INFORMATION" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### Study/project title:" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### Description:" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### Principle Investigator" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### Link to Data management plan" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "### DATA ORGANIZATION" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### Link to Data Storage" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### Folder structure:" >> $(DIR)/README.md
	@echo "\`\`\`" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "\`\`\`" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### File naming conventions:" >> $(DIR)/README.md
	@echo "<provide explanation of the elements used, allowed values and examples>" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "<DATE>_<PI_INITIAL>_<PROJECT_ID>_<DATASET>_<DESCRIPTION>_<DONE_BY>_<VERSION_NUMBER>.<FILE_FORMAT>" >> $(DIR)/README.md
	@echo "" >> $(DIR)/README.md
	@echo "#### File formats:" >> $(DIR)/README.md
	@echo "<Provide a list of all file formats present in this dataset>" >> $(DIR)/README.md
	@echo "Project structure created in $(DIR)."

# Optional: Git initialization
git:
	@cd $(DIR) && git init
	@echo "# Ignore unnecessary files" > $(DIR)/.gitignore
	@echo "*.log" >> $(DIR)/.gitignore
	@echo "*.tmp" >> $(DIR)/.gitignore
	@echo "*.DS_Store" >> $(DIR)/.gitignore
	@echo "__pycache__/" >> $(DIR)/.gitignore
	@echo "Git repository initialized in $(DIR)."
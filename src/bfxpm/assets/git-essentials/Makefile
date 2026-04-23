# === CONFIGURATION ===
TEMPLATE_REPO = https://github.com/JD2112/git-essentials.git
TEMPLATE_BRANCH = main
TEMP_DIR = .template-tmp

FILES = \
	CITATION.cff \
	CODE_OF_CONDUCT.md \
	CODEOWNERS.md \
	CONTRIBUTION \
	LICENSE \
	SECURITY.md \
	SUPPORT.md \
	README.md

GITHUB_DIRS = \
	ISSUE_TEMPLATE

# === MAIN TARGET ===

.PHONY: add-templates clean-template

add-templates: clone-template copy-files copy-github-dirs clean-template
	@echo "✅ All files copied and staged for commit."

# === STEPS ===

clone-template:
	@echo "🔁 Cloning $(TEMPLATE_REPO)..."
	@git clone --depth=1 --branch $(TEMPLATE_BRANCH) $(TEMPLATE_REPO) $(TEMP_DIR)

copy-files:
	@echo "📄 Copying standard files..."
	@for file in $(FILES); do \
		if [ -f "$(TEMP_DIR)/$$file" ]; then \
			cp "$(TEMP_DIR)/$$file" "$$file"; \
			git add "$$file"; \
			echo "✅ Added $$file"; \
		else \
			echo "⚠️  Missing: $$file"; \
		fi \
	done

copy-github-dirs:
	@echo "📂 Copying .github directories..."
	@mkdir -p .github
	@for dir in $(GITHUB_DIRS); do \
		if [ -d "$(TEMP_DIR)/$$dir" ]; then \
			mkdir -p ".github/$$dir"; \
			cp -r "$(TEMP_DIR)/$$dir/"* ".github/$$dir/"; \
			git add ".github/$$dir"; \
			echo "✅ Added .github/$$dir"; \
		else \
			echo "⚠️  Missing directory: $$dir"; \
		fi \
	done

clean-template:
	@rm -rf $(TEMP_DIR)
	@echo "🧹 Cleaned up temporary directory."

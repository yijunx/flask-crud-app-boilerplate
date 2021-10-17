migrate:
	@bash scripts/migration.sh

up:
	@bash scripts/migration.sh
	@bash scripts/start.sh

test:
	@bash scripts/migration.sh
	@bash scripts/test.sh
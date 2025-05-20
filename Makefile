# Diretórios
SRC_DIR := ../dARK
DEST_DIR := config
#venv
VENV_DIR := .venv
REQ_FILE := requirements.txt


# Alvo padrão
all: copy

copy:
	@mkdir -p $(DEST_DIR)
	cp $(SRC_DIR)/config.ini $(DEST_DIR)/
	cp -r $(SRC_DIR)/deployed_contracts.ini $(DEST_DIR)/

venv:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r $(REQ_FILE)
	
clean:
	rm -rf $(DEST_DIR)/*.ini
#rm -rf $(VENV_DIR)

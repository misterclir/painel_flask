import os
import logging

logger = logging.getLogger(__name__)

class ItemDatabase:
    def __init__(self, file_path=None):
        self.items = {}
        if file_path:
            self.load_from_file(file_path)
    
    def load_from_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                logger.warning(f"Arquivo Item.txt não encontrado em: {file_path}")
                return False

            current_category = None
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.isdigit():
                        current_category = int(line)
                    elif line and not line.startswith('//') and not line == 'end':
                        parts = line.split(maxsplit=1)
                        if len(parts) >= 2:
                            item_index = int(parts[0])
                            item_name = parts[1].strip('"')
                            self.items[f"{current_category},{item_index}"] = item_name
                            logger.debug(f"Item carregado: {current_category},{item_index} -> {item_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar base de itens: {str(e)}")
            return False
    
    def get_item_name(self, cat, index):
        return self.items.get(f"{cat},{index}", f"Item {cat}-{index}")
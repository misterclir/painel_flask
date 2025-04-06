import xml.etree.ElementTree as ET
import os
from tools.utils.item_database import ItemDatabase

class ItemBagEditor:
    def __init__(self, xml_path, item_db_path='data/Item.txt'):
        self.xml_path = xml_path
        self.item_db = ItemDatabase(item_db_path) if os.path.exists(item_db_path) else None
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
    
    def load_items(self):
        """Carrega os itens do XML para edição"""
        items = []
        
        for drop_section in self.root.findall(".//DropSection"):
            for drop_allow in drop_section.findall(".//DropAllow"):
                for drop in drop_allow.findall(".//Drop"):
                    for item in drop.findall(".//Item"):
                        item_data = {
                            'cat': item.get('Cat'),
                            'index': item.get('Index'),
                            'name': self.get_item_name(item.get('Cat'), item.get('Index')),
                            'skill': item.get('Skill', '0'),
                            'luck': item.get('Luck', '0'),
                            'option': item.get('Option', '0'),
                            'exc': item.get('Exc', '-1'),
                            'setitem': item.get('SetItem', '0'),
                            'socketcount': item.get('SocketCount', '0'),
                            'duration': item.get('Duration', '0'),
                            'min_level': item.get('ItemMinLevel', '0'),
                            'max_level': item.get('ItemMaxLevel', '0')
                        }
                        items.append(item_data)
        
        return items
    
    def save_changes(self, form_data):
        """Salva as alterações no arquivo XML"""
        item_counter = 0
        
        for drop_section in self.root.findall(".//DropSection"):
            for drop_allow in drop_section.findall(".//DropAllow"):
                for drop in drop_allow.findall(".//Drop"):
                    for item in drop.findall(".//Item"):
                        prefix = f"item_{item_counter}_"
                        
                        item.set('Skill', form_data.get(f"{prefix}skill", '0'))
                        item.set('Luck', form_data.get(f"{prefix}luck", '0'))
                        item.set('Option', form_data.get(f"{prefix}option", '0'))
                        item.set('Exc', form_data.get(f"{prefix}exc", '-1'))
                        item.set('SetItem', form_data.get(f"{prefix}setitem", '0'))
                        item.set('SocketCount', form_data.get(f"{prefix}socketcount", '0'))
                        item.set('Duration', form_data.get(f"{prefix}duration", '0'))
                        item.set('ItemMinLevel', form_data.get(f"{prefix}min_level", '0'))
                        item.set('ItemMaxLevel', form_data.get(f"{prefix}max_level", '0'))
                        
                        item_counter += 1
        
        # Salvar o arquivo XML modificado
        self.tree.write(self.xml_path, encoding='utf-8', xml_declaration=True)
    
    def get_item_name(self, cat, index):
        """Obtém o nome do item da base de dados"""
        if not self.item_db:
            return f"Item {cat}-{index}"
        return self.item_db.get_item_name(cat, index)
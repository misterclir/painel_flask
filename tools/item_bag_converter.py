import xml.etree.ElementTree as ET
import os
import re
import logging
import zipfile
from pathlib import Path
from flask import current_app
from tools.utils.item_database import ItemDatabase

logger = logging.getLogger(__name__)

class ItemBagConverter:
    def __init__(self, item_db_path=None):
        self.version = "1.1.8"
        self.item_db = ItemDatabase(item_db_path) if item_db_path else None
    
    def convert_multiple_xml_to_txt(self, xml_files, output_dir):
        """Converts multiple XML files to TXT and returns a ZIP path"""
        try:
            # Create unique temp directory
            temp_dir = os.path.join(output_dir, "temp_conversion")
            os.makedirs(temp_dir, exist_ok=True)
            
            converted_files = []
            for xml_file in xml_files:
                result = self.convert_xml_to_txt(xml_file, temp_dir)
                if result and result.get('status'):
                    converted_files.append(result['output_path'])
            
            if not converted_files:
                return None
            
            # Create ZIP
            zip_filename = "converted_files.zip"
            zip_path = os.path.join(output_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in converted_files:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
            
            # Cleanup temp files
            for file_path in converted_files:
                try:
                    os.remove(file_path)
                except:
                    pass
            
            return zip_path
        except Exception as e:
            current_app.logger.error(f"Error converting multiple files: {str(e)}")
            return None
    
    def convert_xml_to_txt(self, xml_file_path, output_dir=None):
        """Converts a single XML file to TXT format"""
        try:
            # Basic file validation
            if not os.path.exists(xml_file_path) or os.path.getsize(xml_file_path) == 0:
                return {
                    'status': False,
                    'message': 'File does not exist or is empty',
                    'output_path': None
                }

            # Parse XML
            try:
                tree = ET.parse(xml_file_path)
                root = tree.getroot()
            except ET.ParseError as e:
                return {
                    'status': False,
                    'message': f'XML parsing error: {str(e)}',
                    'output_path': None
                }

            # Validate root element
            if root.tag != "ItemBag":
                return {
                    'status': False,
                    'message': 'Invalid XML structure - root tag should be "ItemBag"',
                    'output_path': None
                }

            # Process configuration
            bag_config = root.find(".//BagConfig")
            money_drop = bag_config.get('MoneyDrop', '0') if bag_config is not None else '0'
            
            # Process drop sections
            drop_sections = root.findall(".//DropSection")
            if not drop_sections:
                return {
                    'status': False,
                    'message': 'No drop sections found. Verify XML contains <DropSection> tags',
                    'output_path': None
                }

            # Generate output filename
            base_name = os.path.basename(xml_file_path)
            txt_filename = self._rename_output_file(base_name)
            
            if output_dir:
                output_dir = Path(output_dir)
                os.makedirs(output_dir, exist_ok=True)
                output_path = output_dir / txt_filename
            else:
                output_path = Path(xml_file_path).with_name(txt_filename)

            # Generate TXT content
            txt_content = self._generate_txt_content(root, drop_sections, money_drop)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            
            return {
                'status': True,
                'message': 'Conversion successful',
                'output_path': str(output_path)
            }
            
        except Exception as e:
            current_app.logger.error(f"Critical conversion error: {str(e)}")
            return None

    def _rename_output_file(self, base_name):
        """Renames output file according to X-Team standards"""
        name = base_name.replace('.xml', '')
        
        if name.startswith('Event_'):
            name = name.replace('Event_', '').replace('_Reward', ' Reward')
            return name.replace('_', ' ') + '.txt'
        elif name.startswith('Item_'):
            name = re.sub(r'Item_\(\d+,\d+,\d+\)_', '', name)
            return name.replace('_', ' ') + '.txt'
        elif name.startswith('Monster_'):
            name = re.sub(r'Monster_\(\d+\)_', '', name)
            return name.replace('_', ' ') + '.txt'
        else:
            name = name.replace('_Reward', ' Reward')
            return name + '.txt'

    def _generate_txt_content(self, root, drop_sections, money_drop):
        """Generates TXT content in X-Team format with proper comment formatting"""
        txt_lines = []
        
        # Section 0 - Basic settings
        txt_lines.append("0")
        txt_lines.append("//Index\tDropRate")
        for i, _ in enumerate(drop_sections):
            txt_lines.append(f"{i}\t10000")
        txt_lines.append("end\n")
        
        # Section 1 - Class settings
        txt_lines.append("1")
        txt_lines.append("//Index\tSection\tSectionRate\tMoneyAmount\tOptionValue\tDW\tDK\tFE\tMG\tDL\tSU\tRF\tGL\tRW\tSL\tGC\tKM\tLM\tIK")
        
        ruud = root.find('.//Ruud')
        money_amount = ruud.get('MaxValue', '0') if ruud is not None else '0'
        option_value = '16' if ruud is not None else '0'
        section_counter = 2
        
        for index, section in enumerate(drop_sections):
            drop_allows = section.findall('.//DropAllow')
            
            # Ruud section
            ruud_rate = ruud.get('GainRate', '0') if ruud is not None else '0'
            txt_lines.append(f"{index}\t2\t{ruud_rate}\t{money_amount}\t{option_value}\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1")
            section_counter = 3
            
            for drop_allow in drop_allows:
                drops = drop_allow.findall('.//Drop')
                for drop in drops:
                    section_rate = drop.get('Rate', '10000')
                    classes = {
                        'DW': drop_allow.get('DW', '1'),
                        'DK': drop_allow.get('DK', '1'),
                        'FE': drop_allow.get('ELF', '1'),
                        'MG': drop_allow.get('MG', '1'),
                        'DL': drop_allow.get('DL', '1'),
                        'SU': drop_allow.get('SU', '1'),
                        'RF': drop_allow.get('RF', '1'),
                        'GL': drop_allow.get('GL', '1'),
                        'RW': drop_allow.get('RW', '1'),
                        'SL': drop_allow.get('SLA', '1'),
                        'GC': drop_allow.get('GC', '1'),
                        'KM': drop_allow.get('LW', '1'),
                        'LM': drop_allow.get('LM', '1'),
                        'IK': drop_allow.get('IK', '1')
                    }
                    class_line = "\t".join(classes.values())
                    txt_lines.append(f"{index}\t{section_counter}\t{section_rate}\t0\t0\t{class_line}")
                    section_counter += 1
        
        txt_lines.append("end\n")
        
        # Item sections with proper comment formatting
        section_counter = 3
        for section in drop_sections:
            drop_allows = section.findall('.//DropAllow')
            for drop_allow in drop_allows:
                drops = drop_allow.findall('.//Drop')
                for drop in drops:
                    txt_lines.append(f"{section_counter}")
                    txt_lines.append("//Index\tLevel\tGrade\tOption0\tOption1\tOption2\tOption3\tOption4\tOption5\tOption6\tDuration\tComment")
                    
                    for item in drop.findall('.//Item'):
                        cat = item.get('Cat', '0')
                        idx = item.get('Index', '0')
                        min_lvl = item.get('ItemMinLevel', '0')
                        max_lvl = item.get('ItemMaxLevel', min_lvl)
                        level = f"{min_lvl}-{max_lvl}" if min_lvl != max_lvl else min_lvl
                        
                        item_data = {
                            'index': f"{cat},{idx}",
                            'level': level,
                            'grade': '0',
                            'opt0': '-1',
                            'opt1': '1' if item.get('Skill', '0') == '1' else '0',
                            'opt2': '1' if item.get('Luck', '0') == '1' else '0',
                            'opt3': self._map_option(item.get('Option', '0')),
                            'opt4': self._map_exc(item.get('Exc', '-1')),
                            'opt5': self._map_setitem(item.get('SetItem', '0')),
                            'opt6': self._map_socketcount(item.get('SocketCount', '0')),
                            'duration': item.get('Duration', '0') or item.get('Durability', '0'),
                            'comment': f"//{self._get_item_name(cat, idx)}"  # Fixed comment format
                        }
                        
                        line = "\t".join(item_data.values())
                        txt_lines.append(line)
                    
                    txt_lines.append("end\n")
                    section_counter += 1
        
        return "\n".join(txt_lines)

    def _map_option(self, option):
        """Maps XML Option to TXT Option3"""
        option = int(option)
        if option == 0: return '-1'
        elif option == -1: return '11-18'
        elif 1 <= option <= 7: return str(11 + option)
        return '-1'

    def _map_exc(self, exc):
        """Maps XML Exc to TXT Option4"""
        if exc == '-1' or exc == '-10':
            return '-1'
        elif exc == '-2':
            return '12'
        elif exc.startswith('-3;') or exc.startswith('-3:'):
            return '12'
        elif ';' in exc:
            return '-1'
        return '-1'

    def _map_setitem(self, setitem):
        """Maps XML SetItem to TXT Option5"""
        setitem = int(setitem)
        if setitem == 0: return '0'
        elif setitem == 1: return '2'
        return '0'

    def _map_socketcount(self, socketcount):
        """Maps XML SocketCount to TXT Option6"""
        socketcount = int(socketcount)
        if socketcount == 0: return '0'
        elif socketcount == 1: return '12'
        elif socketcount == 2: return '13'
        elif socketcount == 3: return '14'
        elif socketcount == 4: return '15'
        elif socketcount == 5: return '16'
        elif socketcount == -1: return '5'
        return '0'

    def _get_item_name(self, cat, index):
        """Gets item name from database with fallback"""
        if not self.item_db:
            return f"Item {cat}-{index}"
        return self.item_db.get_item_name(cat, index)
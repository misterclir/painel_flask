from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from tools.utils.item_editor import ItemBagEditor
from config import Config

editor_bp = Blueprint('item_editor', __name__, url_prefix='/item-editor')

@editor_bp.route('/', methods=['GET', 'POST'])
def item_editor():
    if request.method == 'POST':
        # Verificar se é um upload de arquivo ou edição
        if 'xml_file' in request.files:
            return handle_file_upload()
        elif 'save_changes' in request.form:
            return handle_save_changes()
    
    return render_template('tools/item_bag_editor.html')

def handle_file_upload():
    """Processa o upload de arquivo XML"""
    file = request.files['xml_file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('item_editor.item_editor'))
    
    if file and file.filename.endswith('.xml'):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(Config.UPLOAD_FOLDER, 'item_editor')
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        # Carregar o arquivo para edição
        editor = ItemBagEditor(filepath)
        items_data = editor.load_items()
        
        return render_template('tools/item_bag_editor.html', 
                            items=items_data,
                            filename=filename)
    
    flash('Por favor, envie um arquivo XML válido', 'danger')
    return redirect(url_for('item_editor.item_editor'))

def handle_save_changes():
    """Salva as alterações no arquivo XML"""
    filename = request.form.get('filename')
    if not filename:
        flash('Nenhum arquivo carregado para edição', 'danger')
        return redirect(url_for('item_editor.item_editor'))
    
    upload_dir = os.path.join(Config.UPLOAD_FOLDER, 'item_editor')
    filepath = os.path.join(upload_dir, filename)
    
    if not os.path.exists(filepath):
        flash('Arquivo original não encontrado', 'danger')
        return redirect(url_for('item_editor.item_editor'))
    
    # Processar as alterações
    editor = ItemBagEditor(filepath)
    try:
        editor.save_changes(request.form)
        flash('Alterações salvas com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao salvar alterações: {str(e)}', 'danger')
    
    # Recarregar os dados atualizados
    items_data = editor.load_items()
    return render_template('tools/item_bag_editor.html',
                         items=items_data,
                         filename=filename)
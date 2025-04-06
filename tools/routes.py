from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
import zipfile
from tools.item_bag_converter import ItemBagConverter
from config import Config

tools_bp = Blueprint('tools_bp', __name__, url_prefix='/tools')

@tools_bp.route('/item-bag-converter', methods=['GET', 'POST'])
def item_bag_converter():
    item_db_path = os.path.join(current_app.root_path, 'data', 'Item.txt')
    
    if request.method == 'POST':
        if 'xml_files' not in request.files:
            flash('Nenhum arquivo enviado', 'danger')
            return redirect(request.url)
        
        files = request.files.getlist('xml_files')
        if not files or all(file.filename == '' for file in files):
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        
        valid_files = []
        upload_dir = os.path.join(Config.UPLOAD_FOLDER, 'item_bags')
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            if file and file.filename.endswith('.xml'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                valid_files.append(file_path)
        
        if not valid_files:
            flash('Nenhum arquivo XML válido encontrado', 'danger')
            return redirect(request.url)
        
        output_dir = os.path.join(Config.UPLOAD_FOLDER, 'converted')
        os.makedirs(output_dir, exist_ok=True)
        
        converter = ItemBagConverter(item_db_path if os.path.exists(item_db_path) else None)
        
        if len(valid_files) == 1:
            result = converter.convert_xml_to_txt(valid_files[0], output_dir)
            if not result:
                flash('Ocorreu um erro crítico durante a conversão', 'danger')
            elif result.get('status'):
                flash(result['message'], 'success')
                output_filename = os.path.basename(result['output_path'])
                return render_template('tools/item_bag_converter.html', 
                                    download_file=output_filename,
                                    version=converter.version,
                                    has_item_db=os.path.exists(item_db_path))
            else:
                flash(result['message'], 'danger')
        else:
            zip_path = converter.convert_multiple_xml_to_txt(valid_files, output_dir)
            if not zip_path:
                flash('Falha ao criar arquivo ZIP com os arquivos convertidos', 'danger')
            else:
                flash(f'{len(valid_files)} arquivos convertidos com sucesso!', 'success')
                zip_filename = os.path.basename(zip_path)
                return render_template('tools/item_bag_converter.html',
                                    download_zip=zip_filename,
                                    version=converter.version,
                                    has_item_db=os.path.exists(item_db_path))
    
    return render_template('tools/item_bag_converter.html', 
                         version='1.1.7',
                         has_item_db=os.path.exists(item_db_path))

@tools_bp.route('/download-converted/<filename>', endpoint='download_converted_file')
def download_converted(filename):
    download_dir = os.path.join(Config.UPLOAD_FOLDER, 'converted')
    try:
        return send_from_directory(download_dir, filename, as_attachment=True)
    except FileNotFoundError:
        flash('Arquivo não encontrado para download', 'danger')
        return redirect(url_for('tools_bp.item_bag_converter'))

@tools_bp.route('/download-converted-zip/<filename>', endpoint='download_converted_zip')
def download_converted_zip(filename):
    download_dir = os.path.join(Config.UPLOAD_FOLDER, 'converted')
    try:
        return send_from_directory(download_dir, filename, as_attachment=True, mimetype='application/zip')
    except FileNotFoundError:
        flash('Arquivo ZIP não encontrado', 'danger')
        return redirect(url_for('tools_bp.item_bag_converter'))
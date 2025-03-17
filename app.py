from flask import Flask, render_template, request, send_file, jsonify
import os
import zipfile
from helper import parseFromDirectory
import shutil
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400

    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'El archivo debe ser .zip'}), 400
        
    # Get the file type from form data
    file_type = request.form.get('type', 'default')
    
    # Create unique working directory
    session_id = str(uuid.uuid4())
    work_dir = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(work_dir)

    # Store original filename and file type
    original_filename = file.filename
    with open(os.path.join(work_dir, 'original_filename.txt'), 'w') as f:
        f.write(original_filename)
    with open(os.path.join(work_dir, 'file_type.txt'), 'w') as f:
        f.write(file_type)

    # Save and extract zip
    zip_path = os.path.join(work_dir, 'input.zip')
    file.save(zip_path)
    
    extract_dir = os.path.join(work_dir, 'input')
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Skip macOS system files and directories
            if '__MACOSX' in member or member.startswith('._') or os.path.basename(member).startswith('._'):
                continue
                
            filename = os.path.basename(member)
            if not filename:
                continue
            source = zip_ref.open(member)
            target = open(os.path.join(extract_dir, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

    # Create output directory inside the session work_dir
    output_dir = os.path.join(work_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Call parseFromDirectory with file_type parameter
    parseFromDirectory(extract_dir, output_dir, file_type)

    # Zip the modified PDFs from output_dir
    result_zip = os.path.join(work_dir, 'output.zip')
    with zipfile.ZipFile(result_zip, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)

    # Cleanup
    # shutil.rmtree(extract_dir)
    # os.remove(zip_path)
    # shutil.rmtree(output_dir)

    return jsonify({
        'success': True,
        'session_id': session_id,
        'file_type': file_type
    })

@app.route('/download/<session_id>')
def download(session_id):
    result_zip = os.path.join(UPLOAD_FOLDER, session_id, 'output.zip')
    
    # Read original filename
    filename_path = os.path.join(UPLOAD_FOLDER, session_id, 'original_filename.txt')
    with open(filename_path, 'r') as f:
        original_filename = f.read()
    
    # Create new filename with _procesado before the .zip extension
    base_name = original_filename[:-4]  # remove .zip
    new_filename = f"{base_name}_procesado.zip"
    
    return send_file(
        result_zip,
        as_attachment=True,
        download_name=new_filename
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

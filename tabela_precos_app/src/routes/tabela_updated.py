from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os
from werkzeug.utils import secure_filename

tabela_bp = Blueprint('tabela', __name__)

# Importar os dados da planilha
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
dados_file = os.path.join(current_dir, 'dados_planilha.py')
exec(open(dados_file).read())

@tabela_bp.route('/buscar', methods=['POST'])
def buscar_veiculo():
    """Busca veículos na planilha"""
    data = request.get_json()
    termo_busca = data.get('termo', '').upper().strip()
    
    if not termo_busca:
        return jsonify({'erro': 'Termo de busca não fornecido'}), 400
    
    # Buscar em MODELO, UP e VARIANTE
    resultados = []
    for item in dados_planilha:
        if (termo_busca in item['MODELO'].upper() or 
            termo_busca in item['UP'].upper() or 
            termo_busca in item['VARIANTE'].upper()):
            resultado = {
                'modelo': item['MODELO'],
                'up': item['UP'],
                'variante': item['VARIANTE'],
                'tabela': item['TABELA'],
                'preco_venda': item['PREÇO VENDA'],
                'ano': item['ANO']
            }
            resultados.append(resultado)
    
    return jsonify({
        'resultados': resultados,
        'total': len(resultados)
    })

@tabela_bp.route('/upload', methods=['POST'])
def upload_planilha():
    """Upload de nova planilha (simulado)"""
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    arquivo = request.files['arquivo']
    
    if arquivo.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
    
    if arquivo and arquivo.filename.endswith('.xlsx'):
        # Simular o upload bem-sucedido
        return jsonify({'sucesso': 'Planilha carregada com sucesso (simulado)'})
    
    return jsonify({'erro': 'Formato de arquivo inválido. Use apenas .xlsx'}), 400

@tabela_bp.route('/download-template')
def download_template():
    """Download do template da planilha"""
    try:
        return send_from_directory(
            current_app.static_folder,
            'TabeladepreçoJulho25.25.xlsx',
            as_attachment=True,
            download_name='template_tabela_precos.xlsx'
        )
    except Exception as e:
        return jsonify({'erro': 'Template não encontrado'}), 404

@tabela_bp.route('/status')
def status():
    """Retorna o status da aplicação"""
    return jsonify({
        'planilha_carregada': True,
        'total_registros': len(dados_planilha)
    })


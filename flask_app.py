from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/worlds', methods=['POST'])
def get_worlds():
    """
    Обрабатывает POST запрос и делает запрос к API creative worlds
    """
    try:
        # Получаем данные из тела запроса
        data = request.get_json()
        
        # Проверяем наличие поля 'content' в запросе
        if not data or 'content' not in data:
            return jsonify({'error': 'Missing "content" field in request body'}), 400
        
        content = data['content']
        
        # Формируем URL для первого API
        url1 = f"http://api.creative.justmc.io/public/creative/worlds/get/{content}"
        
        # Делаем запрос к первому API
        response1 = requests.get(url1)
        
        # Проверяем статус ответа
        if response1.status_code != 200:
            return jsonify({
                'error': f'First API returned status code {response1.status_code}',
                'url': url1
            }), response1.status_code
        
        return jsonify({
            'source_url': url1,
            'data': response1.json()
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/user', methods=['POST'])
def get_user():
    """
    Обрабатывает POST запрос и делает запрос к API user info
    """
    try:
        # Получаем данные из тела запроса
        data = request.get_json()
        
        # Проверяем наличие поля 'content' в запросе
        if not data or 'content' not in data:
            return jsonify({'error': 'Missing "content" field in request body'}), 400
        
        content = data['content']
        
        # Формируем URL для второго API
        url2 = f"https://website.justmc.io/user/{content}"
        
        # Делаем запрос ко второму API
        response2 = requests.get(url2)
        
        # Проверяем статус ответа
        if response2.status_code != 200:
            return jsonify({
                'error': f'Second API returned status code {response2.status_code}',
                'url': url2
            }), response2.status_code
        
        return jsonify({
            'source_url': url2,
            'data': response2.json()
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# app.py

from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/api/execute-python', methods=['POST'])
def execute_python():
    # Récupérer l'image et le code Python envoyés depuis l'interface HTML
    image = request.files['image']
    code = request.form['code']

    # Créer le dossier uploads s'il n'existe pas
    save_dir = 'uploads'
    os.makedirs(save_dir, exist_ok=True)

    # Sauvegarder l'image uploadée sous un nom standard pour correspondre à ton code Python
    save_path = os.path.join(save_dir, 'joueur1.jpg')
    image.save(save_path)

    # Écrire le code Python reçu dans un fichier temporaire user_script.py
    with open('user_script.py', 'w') as f:
        f.write(code)

    # Exécuter ce script Python et capturer la sortie (stdout ou stderr)
    result = subprocess.run(['python', 'user_script.py'], capture_output=True, text=True)

    # Retourner la sortie en JSON au frontend
    return jsonify({'output': result.stdout or result.stderr})

if __name__ == '__main__':
    app.run(debug=True)

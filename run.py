from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)




# import os
# from flask import Flask, request, redirect, url_for
# from werkzeug.utils import secure_filename
# from app import create_app


# #app = Flask(__name__)
# app = create_app()

# # Configuration de l'upload
# UPLOAD_FOLDER = 'static/uploads/products'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Fonction pour valider les extensions autorisées
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Vérifier si un fichier est uploadé
#         if 'file' not in request.files:
#             return "Aucun fichier sélectionné."

#         file = request.files['file']

#         if file.filename == '':
#             return "Aucun fichier sélectionné."

#         # Si le fichier est accepté
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)  # Sécuriser le nom du fichier
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Sauvegarder le fichier
#             return redirect(url_for('static', filename=f'uploads/products/{filename}'))

#     # Formulaire d'upload
#     return '''
#     <!doctype html>
#     <title>Upload Image</title>
#     <h1>Uploader une image</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

# if __name__ == "__main__":
#     app.run(debug=True)
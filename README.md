# ClipDrop — version complète locale

Cette version contient une interface HTML/CSS/JS et un backend Python Flask. Le bouton envoie le lien au serveur, qui tente de récupérer le média avec `yt-dlp`.

## Prérequis
- Python 3.10 ou plus récent
- FFmpeg installé et accessible dans le PATH (nécessaire pour convertir l'audio en MP3)

## Installation — Windows
1. Décompressez le ZIP.
2. Ouvrez le dossier `clipdrop_complet` dans VS Code.
3. Ouvrez un terminal dans ce dossier.
4. Créez un environnement virtuel :
   `py -m venv .venv`
5. Activez-le :
   PowerShell : `.\.venv\Scripts\Activate.ps1`
   CMD : `.\.venv\Scripts\activate.bat`
6. Installez les dépendances :
   `pip install -r requirements.txt`
7. Lancez le serveur :
   `python app.py`
8. Ouvrez `http://127.0.0.1:5000` dans Chrome.

## Utilisation
Collez un lien TikTok, choisissez Vidéo MP4 ou Musique MP3, puis cliquez sur le bouton.

## Limitations importantes
- Les téléchargements ne sont pas garantis : TikTok peut changer ses mécanismes, restreindre certains contenus ou bloquer des requêtes.
- MP3 nécessite FFmpeg.
- Utilisez uniquement les contenus que vous possédez ou pour lesquels vous avez l'autorisation de téléchargement. Respectez les droits d'auteur et les conditions de la plateforme.
- Ce serveur est configuré pour une utilisation locale uniquement. Ne le publiez pas sur Internet tel quel ; il faudrait ajouter des limites de débit, gestion du nettoyage des fichiers, validation plus stricte et protections de sécurité.
- Le projet n'est pas affilié à TikTok.

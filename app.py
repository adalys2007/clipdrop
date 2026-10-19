import os
import re
import tempfile
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

ALLOWED_HOSTS = {
    "tiktok.com", "www.tiktok.com", "m.tiktok.com",
    "vm.tiktok.com", "vt.tiktok.com"
}

def is_tiktok_url(value: str) -> bool:
    from urllib.parse import urlparse
    try:
        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        return parsed.scheme in ("http", "https") and (
            host in ALLOWED_HOSTS or host.endswith(".tiktok.com")
        )
    except Exception:
        return False

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/download")
def download_media():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url", "")).strip()
    media_format = data.get("format", "video")

    if not is_tiktok_url(url):
        return jsonify(error="URL TikTok invalide."), 400
    if media_format not in ("video", "audio"):
        return jsonify(error="Format non pris en charge."), 400

    # Download only content you own or have permission to save.
    # yt-dlp may fail if TikTok changes its service or restricts the content.
    temp_dir = tempfile.mkdtemp(prefix="clipdrop_")
    output_template = str(Path(temp_dir) / "%(id)s.%(ext)s")

    options = {
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
        "max_filesize": 200 * 1024 * 1024,  # 200 MB cap
        "socket_timeout": 20,
    }
    if media_format == "audio":
        options.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        options.update({
            "format": "best[ext=mp4]/best",
            "merge_output_format": "mp4",
        })

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = Path(ydl.prepare_filename(info))
            if media_format == "audio":
                filename = filename.with_suffix(".mp3")
            elif not filename.exists():
                # yt-dlp may merge formats into the mp4 extension.
                filename = filename.with_suffix(".mp4")

        if not filename.exists():
            candidates = list(Path(temp_dir).glob("*"))
            candidates = [p for p in candidates if p.is_file()]
            if not candidates:
                return jsonify(error="Aucun fichier n’a été généré. Réessaie avec un autre lien."), 502
            filename = candidates[0]

        safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", filename.name)
        return send_file(
            filename,
            as_attachment=True,
            download_name=safe_name,
            mimetype="audio/mpeg" if media_format == "audio" else "video/mp4",
        )
    except Exception:
        # Keep implementation details out of the public error response.
        app.logger.exception("Media processing failed")
        return jsonify(error=(
            "Impossible de traiter ce lien. La vidéo peut être privée, indisponible, "
            "restreinte, ou nécessiter une version plus récente de yt-dlp."
        )), 502

if __name__ == "__main__":
    # Local development only. Do not expose this server publicly without security review.
    app.run(host="127.0.0.1", port=5000, debug=False)

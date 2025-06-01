print("SCRAPER_API_KEY:", os.getenv("SCRAPER_API_KEY"))
import os
import requests
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
SCRAPER_API_URL = "http://api.scraperapi.com/"

@app.route('/api/download', methods=['GET'])
def download_audio():
    video_url = request.args.get('url')
    ext = request.args.get('ext', 'm4a')
    if not video_url:
        return jsonify({'error': 'Missing url parameter'}), 400
    if not SCRAPER_API_KEY:
        return jsonify({'error': 'Missing SCRAPER_API_KEY env variable'}), 500
    # 测试 ScraperAPI 是否可用
    proxy_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={video_url}"
    try:
        resp = requests.get(proxy_url, timeout=15)
        if resp.status_code != 200:
            return jsonify({'error': f'ScraperAPI failed: {resp.status_code}'}), 502
    except Exception as e:
        return jsonify({'error': f'ScraperAPI request failed: {str(e)}'}), 502
    ydl_opts = {
        'format': f'bestaudio[ext={ext}]',
        'quiet': True,
        'skip_download': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            audio_url = None
            # 优先选英语音轨
            for f in formats:
                if f.get('ext') == ext and f.get('acodec') != 'none' and f.get('language') == 'en':
                    audio_url = f.get('url')
                    break
            # 没有英语音轨则选任意音轨
            if not audio_url:
                for f in formats:
                    if f.get('ext') == ext and f.get('acodec') != 'none':
                        audio_url = f.get('url')
                        break
            if not audio_url:
                return jsonify({'error': f'No audio stream found for ext={ext}'}), 404
            return jsonify({
                'title': info.get('title', ''),
                'url': audio_url,
                'format': ext
            })
    except Exception as e:
        return jsonify({'error': f'yt-dlp failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

#flask--------------------------------------------------------------------------------
from flask import *
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

#services--------------------------------------------------------------------------------
import sys
sys.path.append('./model')
sys.path.append('./utils')
from service import twitterService,pixivService,pydriveService,youtubeService

#=====twitter service=====
"""
query : 検索ワード
date : 今日から何日さかのぼるか
limit : 上限取得画像ツイート数
"""
@app.route('/twitter/base',methods=['POST'])
def twitter_base():
    query = request.json['query'] if 'query' in request.json else ''
    date = request.json['date'] if 'date' in request.json else 30
    limit = request.json['limit'] if 'limit' in request.json else 3000
    if query != '':
        twitterService.base_download(query,date,limit)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'query_empty'})
    
@app.route('/twitter/holo',methods=['POST'])
def twitter_holo():
    date = request.json['date'] if 'date' in request.json else 30
    limit = request.json['limit'] if 'limit' in request.json else 3000
    
    twitterService.holo_download(date,limit)
    return jsonify({'status': 'success'})
    
@app.route('/twitter/hololist',methods=['GET'])
def twitter_hololist():
    tags = twitterService.hololist()
    return jsonify({'status': tags})

#===== pixiv service =====
"""
query : 検索ワード
r : 1ならR18のみダウンロード
update : 昨日か今日ダウンロードしてたなら、ダウンロードしない
"""
@app.route('/pixiv/base',methods=['POST'])
def pixiv_base():
    query = request.json['query'] if 'query' in request.json else ''
    r = request.json['r'] if 'r' in request.json else 1
    update = request.json['update'] if 'update' in request.json else True
    pixivService.basePixivDownload(query,r,update)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'query_empty'})
    
@app.route('/pixiv/holo',mothod=['POST'])
def pixiv_holo():
    r = request.json['r'] if 'r' in request.json else 1
    pixivService.holoPixivDownload(r)
    return jsonify({'status': 'success'})

#===== youtube service =====
"""
url : ダウンロードするurl
"""
@app.route('/youtube/mp3',mothod=['POST'])
def youtube_mp3():
    url = request.json['url'] if 'r' in request.json else ''
    if url != '':
        youtubeService.download_mp3(url)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'query_empty'})
    
@app.route('/youtube/mp4',mothod=['POST'])
def youtube_mp4():
    url = request.json['url'] if 'r' in request.json else ''
    if url != '':
        youtubeService.download_mp4(url)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'query_empty'})
    
if __name__ == '__main__':
    app.run(port=2207)
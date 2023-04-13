#Import--------------------------------------------------memo
import pandas as pd
from tqdm import tqdm
import snscrape.modules.twitter as sntwitter
import time
import os
import urllib
import datetime
import yaml
import sys
from pathlib import Path
import timeout_decorator as td
import shutil

sys.path.append('../../utils')
import utilDatetime
import utilFile
from line import message
#Option--------------------------------------------------
class options:
    limit_date = 30
    limit_tweets = 3000
    dir_name = '/root/opt'
    
    yaml_path = os.path.join(dir_name,'option/twitter2_output.yaml')
    with open(yaml_path) as file:
        yml = yaml.safe_load(file)
        
    base_database = yml['base']['database']
    base_image = yml['base']['image']
    holo_database = yml['holo']['database']
    holo_image = yml['holo']['image']
    user_database = yml['user']['database']
    user_image = yml['user']['image']
    
    holo_list = os.path.join(dir_name,'option/HoloFanArt.csv')
    df=pd.read_csv(holo_list, index_col=0)
    word_list=df['FanArt'].tolist()
#Sub Funtion--------------------------------------------------
#optionを更新する
def update_options(date = 30,limit = 3000):
    options.limit_date = date
    options.limit_tweets = limit
    print(f'date : {options.limit_date} ,\n limit : {options.limit_tweets}')
    message(f'date : {options.limit_date} ,\n limit : {options.limit_tweets}')

#ツイートを取得
def get_tweets(query , mode):
    print(f'get tweets {query}...')
    if mode == 'user':
        scraper = sntwitter.TwitterUserScraper(query)
    else:
        scraper = sntwitter.TwitterSearchScraper(query)
    tweets = []
    today = datetime.datetime.today()
    for index,tweet in enumerate(scraper.get_items()):
        images = []
        #スパム対策で高評価4以上のみ取得
        if tweet.likeCount > 4:
            try:
                for media in tweet.media:
                    images.append(media.fullUrl)

                data = [
                    tweet.url, #ツイート元URL
                    [media.fullUrl for media in tweet.media],#画像URL
                    tweet.date,#ツイート日時
                    tweet.user.username,#ツイートした人のid
                    tweet.user.displayname,#ツイートした人の名前
                    tweet.likeCount,#高評価数
                ]
                if len(tweet.media) > 0:
                    tweets.append(data)
            except:
                pass
        
        #ツイートと今日の日付がlimit_date日以上の差があれば終了
        rep_date = tweet.date.replace(tzinfo=None)
        if (today - rep_date).days >= options.limit_date:
            break
        
        #limit_tweets枚を上限(時間がかかるため)
        if(len(tweets) > options.limit_tweets):
            break
        
        #進捗print
        if(len(tweets) % 100 == 0 and len(tweets) > 0):
            print('\rTweet count : {0}'.format(len(tweets)), end="")
    
    #breakしたら、データフレームにして保存する
    tweet_df = pd.DataFrame(
        tweets,columns = ["url","images","date","userId","userName","likeCount"]
    )
    return tweet_df

#ツイートのデータフレームの保存先取得
def get_save_csv(mode,query):
    if mode == 'base':
        csv_path = os.path.join(options.base_database,f'{query}_database.csv')
    if mode == 'holo':
        csv_path = os.path.join(options.holo_database,f'{query}_database.csv')
    if mode == 'user':
        csv_path = os.path.join(options.user_database,f'{query}_database.csv')
    utilFile.make_folder(os.path.dirname(csv_path))
    return csv_path

#データフレームをマージする
def marge_dataframe(tweet_df,csv_path):
    if os.path.exists(csv_path):
        before_df = pd.read_csv(csv_path,index_col=None)
        marged = pd.merge(tweet_df, before_df, on='url', how='outer')
        
        #結合後のデータフレームの列を条件にしてデータを更新する
        marged['date'] = marged['date_y'].fillna(marged['date_x'])
        marged['images'] = marged['images_y'].fillna(marged['images_x'])
        marged['userId'] = marged['userId_y'].fillna(marged['userId_x'])
        marged['userName'] = marged['userName_x'].fillna(marged['userName_y'])
        marged['likeCount'] = marged['likeCount_x'].fillna(marged['likeCount_y'])
        
        result = marged[['url','date','images','userId','userName','likeCount']]#結合後のデータフレーム
        return result
    else:
        return tweet_df
    
#URLを指定して画像を保存する
@td.timeout(5)
def image_download(url,save_path):
    try:
        if not os.path.exists(save_path):
            try:
                response = urllib.request.urlopen(url, timeout=10)
            except:
                pass
            else:
                if response.status == 200:
                    try:
                        with open(save_path, "wb") as f:
                            f.write(response.read())
                            time.sleep(0.5)
                    except:
                        pass
    except:
        pass
    finally:
        if os.path.exists(save_path):
            if os.path.getsize(save_path) == 0:
                os.remove(save_path)

#ALLでの画像保存先を取得
def get_save_path_all(url,mode,query):
    file_name = url.split('/')[-1].split('?')[0]+'.jpg'
    if mode == 'base':
        save_path = os.path.join(options.base_image,query,'All',file_name)
    if mode == 'holo':
        save_path = os.path.join(options.holo_image,query,'All',file_name)
    if mode == 'user':
        save_path = os.path.join(options.user_image,query,'All',file_name)
    folder = os.path.dirname(save_path)
    utilFile.make_folder(folder)
    return save_path

#日付で画像を保存する
def save_date_image(date,image_path,mode,query):
    year = str(date.year)
    month = str(date.month).zfill(2)
    
    now_week = pd.to_datetime(date).week
    first_date = date.replace(day = 1)
    start_week = pd.to_datetime(first_date).week
    if date.month == 1:
        start_week = 1
    
    week_num = now_week - start_week + 1
    if(week_num < 0):
        week_num = 0
    week_str = str(week_num).zfill(2)
    date_dir = year + month + week_str
    
    file_name = os.path.basename(image_path)
    if mode == 'base':
        save_path = os.path.join(options.base_image,query,'Date',date_dir,file_name)
    if mode == 'holo':
        save_path = os.path.join(options.holo_image,query,'Date',date_dir,file_name)
    if mode == 'user':
        save_path = os.path.join(options.user_image,query,'Date',date_dir,file_name)
    
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    if not os.path.exists(save_path):
        shutil.copyfile(image_path,save_path)
        
#高評価別の画像の保存先を取得
def get_good_save_path(good,image_path,mode,query):
    file_name = os.path.basename(image_path)
    if mode == 'base':
        #set save path
        if good >= 10000:
            save_path = os.path.join(options.base_image,query,'Good','10000_More',file_name)
        if 10000 > good and good >= 5000:
            save_path = os.path.join(options.base_image,query,'Good','05000_More',file_name)
        if 5000 > good and good >= 1000:
            save_path = os.path.join(options.base_image,query,'Good','01000_More',file_name)
        if 1000 > good:
            save_path = os.path.join(options.base_image,query,'Good','01000_Under',file_name)
            
    if mode == 'holo':
        #set save path
        if good >= 10000:
            save_path = os.path.join(options.holo_image,query,'Good','10000_More',file_name)
        if 10000 > good and good >= 5000:
            save_path = os.path.join(options.holo_image,query,'Good','05000_More',file_name)
        if 5000 > good and good >= 1000:
            save_path = os.path.join(options.holo_image,query,'Good','01000_More',file_name)
        if 1000 > good:
            save_path = os.path.join(options.holo_image,query,'Good','01000_Under',file_name)
            
    if mode == 'user':
        #set save path
        if good >= 10000:
            save_path = os.path.join(options.user_image,query,'Good','10000_More',file_name)
        if 10000 > good and good >= 5000:
            save_path = os.path.join(options.user_image,query,'Good','05000_More',file_name)
        if 5000 > good and good >= 1000:
            save_path = os.path.join(options.user_image,query,'Good','01000_More',file_name)
        if 1000 > good:
            save_path = os.path.join(options.user_image,query,'Good','01000_Under',file_name)
    return save_path
        
#高評価で画像を保存する
def save_good_image(good , image_path , mode , query):
    #get save path
    save_path = get_good_save_path(good, image_path , mode , query)
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    
    #すでにほかの場所にあるか調べる
    before_image_path = ''
    for g in [10010 , 5010 , 1010 , 100]:
        test_save_path = get_good_save_path(g , image_path , mode , query)
        if os.path.exists(test_save_path):
            before_image_path = test_save_path
            
    #ローカルにないならそのままsave_pathへコピー
    if before_image_path == '':
        shutil.copyfile(image_path,save_path)
    
    #ローカルにあってsave_pathと異なるなら新しいほうに置き換え
    if before_image_path != '' and before_image_path != save_path:
        os.remove(before_image_path)
        shutil.copyfile(image_path,save_path)
    

#Main Function--------------------------------------------------
def sub_download(query , mode , date , limit):
    update_options(date , limit)# オプション更新
    
    message(f'get tweets {query}')
    tweet_df = get_tweets(query , mode)# ツイート取得
    csv_path = get_save_csv(mode , query)# データフレームの保存先を取得
    marged = marge_dataframe(tweet_df , csv_path)# すでにデータフレームが存在していたらマージする
    tweet_df.to_csv(csv_path)# マージ後のデータフレームを保存する
    
    message(f'get {query} tweets {len(tweet_df)}')
    
    saved = 0
    
    for index,row in tqdm(tweet_df.iterrows(), total=len(tweet_df) , desc='image DL'):#画像のダウンロード&保存処理
        images = row['images']
        for url in images:
            save_path = get_save_path_all(url , mode , query)
            if not os.path.exists(save_path):
                try:
                    image_download(url , save_path)
                except:
                    pass
            
            #ALLにダウンロードできた場合
            if os.path.exists(save_path):
                saved = saved + 1
                date = row['date']
                save_date_image(date , save_path , mode , query)#YYYYMMWWで画像を保存する
                good = row['likeCount']
                save_good_image(good , save_path , mode , query)#高評価別で画像を保存する
    message(f'saved {query} : {saved}')
            
def base_download(query , date = 30,limit = 3000):
    mode = 'base'
    sub_download(query , mode , date,limit)
            
def holo_download(date = 30,limit = 3000):
    mode = 'holo'
    for query in tqdm(options.word_list):
        sub_download(query , mode,date,limit)
        
def user_download(query , date = 30,limit = 3000):
    mode = 'user'
    sub_download(query , mode , date,limit)
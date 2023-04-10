import sys
sys.path.append('../utils')
sys.path.append('../model')
#import twitterModel as tw
import twitter2Model as tw

def base_download(query,args_date = 30,args_tweets = 3000):
    tw.base_download(query,args_date,args_tweets)
    
def holo_download(args_date=30,args_tweets=3000):
    tw.holo_download(args_date,args_tweets)
    
def user_download(query,args_date = 30,args_tweets = 3000):
    tw.user_download(query,args_date,args_tweets)
    
def hololist():
    return tw.get_hololist()
import sys
sys.path.append('./model')
sys.path.append('./utils')
from service import twitterService

date = 1800
limit = 50000
twitterService.holo_download(date,limit)
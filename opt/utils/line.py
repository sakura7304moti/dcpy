#bLg2L6w7MhUXm5eG1Pyz6jB5IJ8PVU3anYX5FbjUbSc
import requests

def message(text):
    # 取得したTokenを代入
    line_notify_token = 'bLg2L6w7MhUXm5eG1Pyz6jB5IJ8PVU3anYX5FbjUbSc'

    # 送信したいメッセージ
    message = text

    # Line Notifyを使った、送信部分
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{message}'}
    requests.post(line_notify_api, headers=headers, data=data)
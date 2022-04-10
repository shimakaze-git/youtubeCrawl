"""Main module."""

import requests
import urllib.parse as parse

#パラメータ設定
apikey = ""


def video_comment_reply(video_id, parent_id, next_page_token=''):

    URL_HEAD = "https://www.googleapis.com/youtube/v3/"

    #APIパラメータセット
    params = {
        'key': apikey,
        'part': 'snippet',
        'videoId': video_id,
        'maxResults': 100,
        'moderationStatus': 'published',
        'order': 'time',
        'pageToken': next_page_token,
        'searchTerms': '',
        'textFormat': 'plainText',
        'parentId': parent_id,
    }

    response = requests.get(URL_HEAD + 'comments', params=params)
    response_json = response.json()

    items = response_json['items']
    for item in items:
        # コメント
        text = item['snippet']['textDisplay']
        text = text.replace('\r', '\n')
        # .replace('\n', ' ')

        # グッド数
        like_cnt = item['snippet']['likeCount']

        # ユーザー名
        user_name = item['snippet']['authorDisplayName']

        print("text child", text)
        print("===" * 20)

    if 'nextPageToken' in response_json:
        video_comment_reply(video_id, parent_id, response_json["nextPageToken"])

def video_comment(video_id, next_page_token=''):
    URL_HEAD = "https://www.googleapis.com/youtube/v3/"

    #APIパラメータセット
    params = {
        'key': apikey,
        'part': 'snippet',
        #----↓フィルタ（いずれか1つ）↓-------
        #'allThreadsRelatedToChannelId':channelId,
        'videoId': video_id,
        #----↑フィルタ（いずれか1つ）↑-------
        'maxResults': 100,
        'moderationStatus': 'published',
        # 'order':'relevance',
        'order': 'time',
        'pageToken': next_page_token,
        'searchTerms': '',
        'textFormat': 'plainText',
    }

    response = requests.get(URL_HEAD + 'commentThreads', params=params)
    response_json = response.json()

    items = response_json['items']

    for item in items:
        # コメント
        text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        text = text.replace('\r', '\n')
        # .replace('\n', ' ')

        # グッド数
        like_cnt = item['snippet']['topLevelComment']['snippet']['likeCount']

        # 返信数
        reply_cnt = item['snippet']['totalReplyCount']

        # ユーザー名
        user_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']

        # Id
        parent_id = item['snippet']['topLevelComment']['id']

        print('text', text)
        print('reply_cnt', reply_cnt)
        # print('{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name, reply_cnt))

        if reply_cnt > 0:
            video_comment_reply(video_id, parent_id)
        print('---' * 20)

    if 'nextPageToken' in response_json:
        video_comment(video_id, response_json["nextPageToken"])

if __name__ == '__main__':
    video_id = "sHjDAm_5dbQ"
    video_comment(video_id)

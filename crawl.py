import os
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def downloadVideo(url, title):
    VIDEO_DIR = os.path.join(os.getcwd(), 'videos')
    ydl_opts = {
        # 'format': 'best',
        # 'format': 'bestvideo',
        'format': '137[ext=mp4]',
        'outtmpl':  '{}/{}'.format(VIDEO_DIR, title) + '.%(ext)s',
        'progress_hooks': [my_hook],
        # 'logger': MyLogger(),
        # 'postprocessors': [
        #     {'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'mp3',
        #      'preferredquality': '192'},
        #     {'key': 'FFmpegMetadata'},
        # ],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    with ydl:
        ydl.extract_info(
            url,
            download=True
        )
        return '{}/{}.mp4'.format(VIDEO_DIR, title)
        # We just want to extract the info


# url = 'https://www.youtube.com/watch?v=6qGiXY1SB68'
# title = 'shibuya_night'
# downloadVideo(url, title)

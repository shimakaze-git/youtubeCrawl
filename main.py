import csv

from crawl import downloadVideo
from extractImage import extractImages


def csvDictList(csv_path='./crawl_list.csv'):
    # encoding="ms932", errors="", newline="" )
    # encoding="ms932", errors="", newline="" )

    csv_path = './crawl_list.csv'
    csv_file = open(csv_path, 'r')

    # 辞書形式
    # f = csv.DictReader(
    #     csv_file,
    #     delimiter=",",
    #     doublequote=True,
    #     lineterminator="\r\n",
    #     quotechar='"',
    #     skipinitialspace=True
    # )

    f = csv.DictReader(csv_file)
    return [row for row in f]


def main():

    csv_list = csvDictList()
    for c in csv_list:
        title = c['title']
        url = c['url']

        try:
            # ダウンロード処理
            pathIn = downloadVideo(url, title)

            print(pathIn)
            print(url, title)

            output = 'output'
            sec = 2

            extractImages(
                pathIn=pathIn,
                pathOut=output,
                sec=sec
            )
        except Exception as e:
            raise e


if __name__ == "__main__":
    main()

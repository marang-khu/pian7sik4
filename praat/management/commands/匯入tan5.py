from os.path import join, isdir

from django.core.management.base import BaseCommand
from textgrid import TextGrid


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from shutil import rmtree
from os import makedirs


class Command(BaseCommand):

    def handle(self, *args, **參數):
        資料目錄 = '/home/Ihc/原始測'

        for 檔名 in ['錄音檔-測試壹-21', '錄音檔-測試貳-21', '錄音檔-測試貳-22']:
            with open(join(資料目錄, 檔名 + '.TextGrid')) as fp:
                grid = TextGrid(fp.read())
                音檔 = 聲音檔.對檔案讀(join(資料目錄, 檔名 + '.wav'))
                新音檔資料夾 = join(資料目錄, 檔名)
                if isdir(新音檔資料夾):
                    rmtree(新音檔資料夾)
                makedirs(新音檔資料夾)
                第幾个新音檔 = 0
                for tier in grid:
                    for 開始時間, 結束時間, 內容 in (tier.simple_transcript):
                        if 內容.strip() not in ['silent']:
                            新音檔 = 音檔.照秒數切出音檔(float(開始時間), float(結束時間))
                            with open(join(
                                新音檔資料夾, '{0:03}.wav'.format(第幾个新音檔)
                            ), 'wb') as 檔案:
                                檔案.write(新音檔.wav格式資料())
                            第幾个新音檔 += 1

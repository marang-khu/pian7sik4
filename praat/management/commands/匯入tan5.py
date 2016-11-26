from os.path import join

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from textgrid import TextGrid


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 版權表


class Command(BaseCommand):

    def handle(self, *args, **參數):
        call_command('顯示資料數量')

        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='Pigu')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '臺北',
            '著作年': '2016',
        }
        資料目錄 = join(settings.BASE_DIR, 'data')

        匯入數量 = 0
        for 檔名 in ['a001-2', 'a002-2', 'a003-2', 'a004-2', ]:
            with open(join(資料目錄, 檔名 + '.TextGrid')) as fp:
                grid = TextGrid(fp.read())
                for tier in grid:
                    json資料 = []
                    for 開始時間, 結束時間, 內容 in (tier.simple_transcript):
                        if 內容.strip() not in ['sounding', 'silent']:
                            json資料.append({
                                '內容': 內容,
                                '語者': '無註明',
                                '開始時間': 開始時間,
                                '結束時間': 結束時間,
                            })
                    影音內容 = {'影音所在': join(資料目錄, 檔名 + '.wav')}
                    影音內容.update(公家內容)
                    影音 = 影音表.加資料(影音內容)

                    聽拍內容 = {'聽拍資料': json資料}
                    聽拍內容.update(公家內容)
                    影音.寫聽拍(聽拍內容)

                    匯入數量 += 1
                    if 匯入數量 % 100 == 0:
                        print('匯入第{}筆：'.format(匯入數量))

        call_command('顯示資料數量')

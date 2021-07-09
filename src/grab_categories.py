import requests
import urllib3
from bs4 import BeautifulSoup as BS
import xlwt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1", cell_overwrite_ok=True)
sheet2 = book.add_sheet("Sheet 2", cell_overwrite_ok=True)



def parse_categ(itt_sheet1,itt_sheet2):
    id_category = 4
    name_categories = []
    r = requests.get('https://mosopttorg.com/', verify=False)
    html = BS(r.content, 'html.parser')
    for el in html.select('div.cat-title'):
        name_category = el.text
        sheet1.write(itt_sheet1, 0, name_category)
        sheet1.write(itt_sheet1, 1, str(itt_sheet1+3))
        name_categories.append(name_category)
        itt_sheet1 += 1
    for el in html.select('div.cat-title a'):
        name = el.attrs['href']
        print(name)
        print(f'Переходим по ссылке {name}')
        r1 = requests.get(name, verify=False)
        html1 = BS(r1.content, 'html.parser')
        a_for_delete = html1.findAll('a', {'class': 'ms_subcategory_product_count'})
        # Удаляем лишние <a> чтобы цикл не проходил два раза
        for match in a_for_delete:
            # После того, как собрали все лишние <a> в a_for_delete, циклом их decopmpose(убираем)
            match.decompose()
        for el in html1.select('div.cat-title a'):
            # теперь в html1 нет тегов <a> которые с количеством продукции
            print('1')
            name = el.attrs['href']
            print(el)
            print(name)
            if 'Количество' not in el.text:
                name_subcategory = el.text
                sheet2.write(itt_sheet2, 0, id_category)
                sheet2.write(itt_sheet2, 1, name_subcategory)
                r2 = requests.get(name, verify=False)
                html2 = BS(r2.content, 'html.parser')
                brands_arr = []
                for el in html2.select('span.ty-product-filters__title'):
                    if el.text == 'Бренд':
                        print('Есть бренд в ' + name)
                        for el in html2.select('ul#content_32_1 li'):
                            if 'Показатьвсе' not in el.text.replace(" ","") and el.text.replace(" ","")!='':
                                print('='+el.text+'=')
                                brands_arr.append(el.text.replace(" ",""))
                                #если добавлять без пробелов, будет куча мусора и дублирующиеся значения не будут чиститься
                brands_arr = list(set(brands_arr))
                #чистим список с дублями посредством преобразования списка в набом - set() и потом обратно в список
                print(type(brands_arr))
                print(brands_arr)
                i=4
                print(len(brands_arr))
                print(len(brands_arr)+4)
                print(i)
                while i<(len(brands_arr)+4):
                    sheet2.write(itt_sheet2, i, brands_arr[i-4])
                    i += 1
                itt_sheet2 += 1
                print(f'Название подкатегории {name_subcategory} Id категории {id_category}')
                print(name)
                book.save("categories.xls")
        id_category += 1



#爬取知乎问题下所有图片
#2017年09月08日

import requests
import re
import json
import os




# url = "https://www.zhihu.com/question/36435092"
def get_headers(id):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Referer":"https://www.zhihu.com/question/" + str(id),
        "authorization":"your auth..."
    }
    return headers

def get_data(url,headers=None):
    response = requests.get(url,headers=headers)
    return response.text

def get_sum(id):
    html = get_data("https://www.zhihu.com/question/" + str(id),get_headers(id))
    pattern = re.compile('<h4 class="List-headerText">.*?<span>(\d+).*?个回答',re.S)
    result = re.findall(pattern,html)
    return result[0]

def make_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)


def main(id):
    make_dir('cat')
    sum = int(get_sum(id))
    print('共有{sum}个回答'.format(sum = sum))

    limit = 20
    offset = 0
    url = "https://www.zhihu.com/api/v4/questions/{id}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={limit}&offset={offset}";
    question_count = 0#应该获取的回答数量，用于偏移量
    question_count_real = 0#真正获取到的回答的数量
    img_count = 0#应该获取到的图片的数量
    img_count_real = 0#真正获取到的图片的数量
    while question_count < sum:
        print('正在获取第{start}到{end}的回答'.format(start = offset + 1, end = offset + limit))
        doc = get_data(url.format(id = id, limit = limit, offset = offset),get_headers(id))
        json_obj = json.loads(doc)
        #获取到的回答列表
        data_list = json_obj.get("data")
        question_t = 0

        #遍历回答
        for data in data_list:
            question_t += 1
            question_count += 1
            question_count_real += 1

            print('\t正在获取第{i}个回答下的图片'.format(i = question_count))
            #获取该回答的内容
            content = data.get("content")

            pattern = re.compile(r'<img.*?class="origin_image zh-lightbox-thumb lazy".*?data-original="(.*?)" data-actualsrc=',re.S)
            #该回答下的图片列表
            img_src_list = re.findall(pattern,content)
            #该回答下的图片的数量
            list_len = len(img_src_list)
            print('\t第{i}个回答下共有{num}张图片'.format(i = question_count,num = list_len))
            img_t = 0
            #遍历每个图片链接，下载图片
            for img_src in img_src_list:
                img_t += 1
                img_count += 1
                img_count_real += 1
                print('\t\t正在获取第{i}个回答下的第{n}张图片，共{num}张图片，总第{sum}张图片'.format(i = question_count,n = img_t,num = list_len,sum = img_count))
                try:
                    with open('cat/' + str(img_count) + ".jpg",'wb') as f:
                        f.write(requests.get(img_src).content)
                except:
                    print('第{n}张图片下载出现异常'.format(n = img_count))
                    img_t -= 1
                    img_count_real -= 1
            print('第{i}个回答下的图片下载完成，下载成功{succ}个，下载失败{fail}个'.format(i = question_count,succ = img_t,fail = (list_len - img_t)))
        print('该页的回答处理完成，成功{succ}个，失败{fail}个'.format(succ = question_t,fail = limit - question_t))
        offset += limit
    print("获取完成，共{count_s}个回答，实际获取{count_r}个回答，共{img_s}张图片，实际获取{img_r}张".format(count_s = sum,count_r = question_count_real,img_s = img_count,img_r = img_count_real))


if __name__ == '__main__':
    id = input('请输入问题id')
    # id = "36435092"
    main(id)
    print("程序结束")
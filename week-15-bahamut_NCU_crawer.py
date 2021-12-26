import urllib.request as req
import bs4
import concurrent.futures
import time

class allart():
    def __init__(self):
        self.arti=""
        self.fl=0
        self.img=""
        self.gp=0
        self.bp=0
        self.reply = list()


totalarti  =0
alla = list()
checkprocess = True

def craw(urls):
    #for urls in urlsk:
    request = req.Request(urls, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")

    titles = root.find_all("div", class_="c-article__content")
    floor = root.find_all("div", class_="c-post__header__author")
    point_ = root.find_all("div" , class_="c-post__body__buttonbar")
    totalreply = root.find_all("div", class_="c-post__footer c-reply")

    global totalarti,alla,checkprocess


    for i,k,p,r in zip(titles , floor,point_,totalreply):
        temp = allart()
        fl = k.find('a')
        gp = p.find("div",class_="gp").find("a").text
        bp = p.find("div",class_="bp").find("a").text
        temp.arti = i.text.strip()
        temp.fl = int(fl['data-floor'])
        reply = r.find_all("article",class_="reply-content__article c-article")
        for re in reply:
            temp.reply.append(re.text)
            #print(re.text)
        if gp!=None:
            temp.gp = int(gp)
        if bp !='-':
            temp.bp = int(bp)
        img = i.find("img", {"class": "lazyload"})
        if img:
            temp.img = img['data-src']
        alla.append(temp)

        totalarti+=1

    if checkprocess:
        checkprocess = False
        print("[Progress]:", end='')
    print('█',end='')
    time.sleep(1)

def max_floor():
    urls = "https://forum.gamer.com.tw/C.php?bsn=60076&snA=4671705&last=1#down"
    request = req.Request(urls, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")
    floor = root.find_all("div", class_="c-post__header__author")
    return floor[-1].find('a')['data-floor']

def pri():
    global alla
    alla = sorted(alla, key=lambda s: s.fl)
    for i in alla:
        print(f"{i.fl}樓 推:{i.gp} 噓:{i.bp} {i.arti}")
        if i.img:
            print(i.img)

def binsearch(num):
    i = 0
    j = len(alla)
    mid = (i+j)//2
    #print(mid)
    while(i<j):
        if alla[mid].fl>num:
            j = mid
            mid = (i+j)//2
        elif alla[mid].fl<num:
            i = mid
            mid = (i + j) // 2
        else:
            return mid
    return -1

def reply(num):
    index = binsearch(int(num))
    if index != -1 :
        if len(alla[index].reply)>0:
            print("-----------------------Reply-----------------------")
            for i in alla[index].reply:
                print(i)
            print("------------------------Done------------------------")
        else:
            print("--------------------目前沒有回覆--------------------")
    else:
        print("---------------------沒有此樓層---------------------")

def end_process():
    while True:
        num = input("重新搜尋請按re , 查詢回復請輸入樓層 , 或按下Enter確認結束:")
        if num == "re":
            return 1
            break
        elif num == "":
            return 0
            break
        else:
            reply(num)
            
def main( ):
    print("【討論】場外中央大學串 @場外休憩區  哈啦板 - 巴哈姆特")
    global totalarti,alla,checkprocess
    while True:
        num = (input("尋找最新消息按1 , 找尋特定頁面請按2:"))
        if(num=="1"):
            urls ="https://forum.gamer.com.tw/C.php?bsn=60076&snA=4671705&last=1#down"
            start_time = time.time()  # 開始時間
            craw(urls)
            print("done")
            pri()
            end_time = time.time()
            print(f"\n執行時間共計{end_time - start_time} 秒,共{totalarti}樓")
            if end_process():
                alla.clear()
                totalarti = 0
                checkprocess = True
            else:
                break

        elif num == "2":

            baseurlfront = "https://forum.gamer.com.tw/C.php?page="
            baseurlbehind = "&bsn=60076&snA=4671705"
            maxf = int(max_floor())
            if (maxf%20)!=0:
                maxf = (maxf//20)+1
            else:
                maxf = maxf//20
            print (f"輸入頁面(1~{maxf+1}):")
            front = int(input())
            behind = int(input())

            urls =  [f"{baseurlfront}{page}{baseurlbehind}" for page in range(front, behind)]
            start_time = time.time()  # 開始時間

            # 同時建立及啟用10個執行緒
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(craw, urls)
            #craw(urls)
            print("done")
            end_time = time.time()

            pri()
            print(f"{end_time - start_time} 秒爬取 {len(urls)} 頁的文章,共{totalarti}樓")
            if end_process():
                alla.clear()
                totalarti = 0
                checkprocess = True
            else:
                break
        else:
            print("錯誤輸入,請在試一次")
if __name__ == "__main__":
  main( )
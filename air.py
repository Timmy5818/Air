import requests
import copy
# 下3行為匯入畫圖套件，我們使用的為matplotlib畫圖
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
# 即時空氣品質指標JSON匯入位置
aqi_url = "https://data.epa.gov.tw/api/v1/aqx_p_432?api_key=1909f878-5d76-4093-9da5-1372086fa7f6"
response = requests.get(aqi_url)
aqi = response.json()['records']

# 測試資料回傳狀況代碼200為正常回傳，404為回傳錯誤
print(response.status_code)
# 下7行為檢查資料是否正常回報
def aqi_none(aqi):
    if len(aqi):
        return
    else:
        print("錯誤，目前無法接收資料")
        exit()
aqi_none(aqi) #呼叫aqi_none函式檢查資料是否正常回報

# si為測量站名稱，將測量站個名稱放入si陣列
# airint為AQI品質，將AQI品質放入air陣列
# pm25air為PM2.5品質，將PM2.5品質放入pm25air陣列
si=[]
airint = []
pm25air = []
for wa in aqi:
    pm25air.append(wa["PM2.5"])
    si.append(wa["SiteName"])
    airint.append(int(wa["AQI"]))
    print(wa["County"] +"  "+ wa["SiteName"]+" "+ "  PM2.5(細懸浮微粒)小時濃度品質:" + wa["PM2.5"] + "  AQI品質:" + wa["AQI"],wa["Status"]) # 顯示各地點測量站的PM2.5及AQI品質
    # 下列3行為PM2.5空值部分取代成數字0
    for i in range(len(pm25air)):   
        if pm25air[i] == "":
            pm25air [i] ='0'

pm25air = list(map(int, pm25air)) # 將pm25air陣列轉換成int型態

# 下列3行程式碼為儲存AQI品質資料為txt檔案，儲存位置為本機C://Users/"您的使用者名稱"內
with open("data_aqi.txt", "w", encoding="utf-8") as file:
     for list in aqi:
        file.write(f'{list["County"]} {list["SiteName"]} {list["AQI"]}\n')

# 下2行為找到AQI中最大的數字，將表示於圖表最大的寬度
max_value = None
max_air =max(airint)

# 下面函式為將AQI品質的顏色進行區分
def bar_color():
    col=[None]*(len(airint)+1)
    col = copy.deepcopy(airint) #要用深複製方式，不然會共用記憶體值會被取代掉
    
    # for key , item in enumerate(col): #也可以使用枚舉
    #     if item >= 0 and item <= 50:
    #         col[key] = "g"

    for key in range(len(col)):
        item = col[key]
        if item >= 0 and item <= 50:
            col[key] = "g" #0~50燈號綠色
        if item >= 51 and item <= 100:
            col[key] = "y" #51~100燈號黃色
        if item >= 101 and item <= 150:
            col[key] = "tab:orange" #101~150燈號橘色
        if item >= 151 and item <= 200:
            col[key] = "r" #151~200燈號紅色
        if item >= 201 and item <= 300:
            col[key] = "m" #201~300燈號紫色
        if item >= 301 and item <= 500:
            col[key] = "tab:brown" #301~500燈號褐紅色
    return col

ylabel_font = {'size':15}
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] #設定字體為微軟正黑體，避免中文亂碼
matplotlib.pyplot.figure(figsize=(15, 10)) #設定圖表的整體大小
y=np.arange(len(si)) #產生 Y 軸座標序列
x=np.arange(0, max_air, 5) #產生 X 軸座標序列
plt.barh(y, airint,color=bar_color()) #繪製AQI品質長條圖
plt.barh(y, pm25air,color="black") #繪製PM2.5長條圖
plt.yticks(y, si) #設定 Y 軸刻度標籤
plt.ylim(0,20) #設定 Y 軸圖表內容上下高度，變可以使用拖移功能
x_ticks=np.arange(0,max_air,5) #X 軸刻度陣列
plt.xticks(x, x_ticks) #設定 X 軸刻度標籤
plt.ylabel('測量站',fontdict = ylabel_font) #設定 Y 軸標題
plt.xlabel('AQI品質及PM2.5品質') #設定 X 軸標題
plt.title('AQI空氣品質及PM2.5品質') #設定 主要 標題
# 下2行將圖表顯示資料標籤
for i, v in enumerate(airint): 
    plt.text(v + 1, i + .0, str(airint[i]), color='black', fontweight='bold',zorder=100)
for i, v in enumerate(pm25air): 
    plt.text(v + 1, i + .0, str(pm25air[i]), color='black', fontweight='bold',zorder=100)

plt.show() #顯示圖表






# 儲存圖片檔案
plt.savefig('./result.png')
plt.clf()




# 其他程式碼
# 下4行為將col產生隨機顏色，但缺點會是有白色
# for i in range(len(airint)+1):
#     if (airint[i] >= 0 )and (airint[i]<= 50):
#         col[i]='g'
#         # col.append(tuple(np.random.choice(range(0, 2), size=3)))
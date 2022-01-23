import time
import pyautogui


WIDTH, HEIGHT = pyautogui.size()            #屏幕宽与高
URL = 'https://www.cc98.org/topic/xxxxxxx/' # 帖子网址
PAGE_NUM = 00                               # 帖子页数
y_offset = 45                               # corner定位时y方向移动距离
x_offset = 130                              # 选中昵称时x方向移动距离


def confirm_input_en():
    # 判断当前输入法，如果为中文，则改回英文
    if pyautogui.locateOnScreen('./img/chinese.png') is not None:
        pyautogui.click('./img/chinese.png')


def get_id():
    # 选中从上往下的第一个id
    x, y = pyautogui.locateCenterOnScreen('./img/corner_upper.png')
    y += y_offset                           # x, y为当前id左侧区域的坐标
    pyautogui.moveTo(x, y)                  # 移动鼠标至当前待获取id的左侧

    # 按下鼠标-向右拖动-放开鼠标，选中当前id
    pyautogui.mouseDown()
    pyautogui.dragRel(x_offset, 0, duration=0.2)
    pyautogui.mouseUp()

    # 将当前id复制到事先打开的记事本中
    pyautogui.hotkey('ctrl', 'c')           # 注意：id长度过短导致复制时会复制到一个回车
    pyautogui.click('./img/notebook.png')   # 点击任务栏的记事本图标
    pyautogui.hotkey('ctrl', 'v')
    confirm_input_en()
    pyautogui.typewrite(',')                # 逗号用作分隔符，与连同部分id复制到的回车相区分

    return x, y


def get_ids_for_page(page):
    while True:
        x, y = get_id()
        pyautogui.moveTo(x, y)              # 光标回到id左侧位置
        pyautogui.click()                   # 点击一下页面，聚焦回到网页

        # 若当前已获取的id太靠近底部，可能使下一楼不显示，对此情况手动向下滚动一定距离
        if HEIGHT - y <= 230:
            pyautogui.scroll(-200)
            y -= 200
            time.sleep(0.5)

        # 通过判断当前已获取的id和最后一个间隙的y坐标大小，确定当前id是否为本页最后一个元素
        intervals = pyautogui.locateAllOnScreen('./img/interval.png')
        last_interval = list(intervals)[-1]
        if y > last_interval.top:           # 若当前id是最后一个元素，则跳出循环
            print('End loop for Page %d.' %page)
            break 

        # 若不是本页最后一个id，则鼠标向下滚动到下一个id附近
        corners = pyautogui.locateAllOnScreen('./img/corner_upper.png')
        c1 = next(corners)
        c2 = next(corners)
        scroll_length = min(int(c1.top - c2.top), int(-c1.top)) # 负值，表示向下滚动
        # scroll函数不太精确，实践发现在后面加一个小的负向滚动可以提升其稳定性
        pyautogui.scroll(scroll_length)
        time.sleep(0.5)
        pyautogui.scroll(-int(0.1*scroll_length))
        time.sleep(0.5)


def switch_page(url, page):
    # 切换帖子页面，默认已聚焦在浏览器中
    pyautogui.hotkey('ctrl', 'e')
    pyautogui.press("backspace")
    confirm_input_en()
    pyautogui.typewrite(url+str(page)+'#1')
    pyautogui.press("enter")
    time.sleep(5)


def get_ids_for_topic(start_page, end_page):
    time.sleep(2)                           # 休眠两秒钟供手动将屏幕切换到浏览器网页处
    for page in range(start_page, end_page+1):
        get_ids_for_page(page)
        if page < end_page:                 # 若已在最后一页则不必继续切换页面
            switch_page(URL, page+1)

    pyautogui.alert('本主题下所有 ID 爬取完毕！')


if __name__ == '__main__':
    get_ids_for_topic(start_page=1, end_page=PAGE_NUM)
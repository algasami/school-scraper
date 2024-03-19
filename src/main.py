from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# consts
STATIC_SITE = "https://www.cac.edu.tw/apply113/system/ColQry_vforStu113apply_GF84ad9zx/new_hiko/m_personal.php"



driver = webdriver.Chrome()

def init():
    driver.get(STATIC_SITE)
    sleep(0.5)
    school_sel = driver.find_element(By.ID, "sel_col")
    return [e.get_attribute("value") for e in school_sel.find_elements(By.TAG_NAME, "option")
            if e.get_attribute("value") != "-1"]

def process_col(col_elem, current_block, last_index):
    btn_layouts = col_elem.find_elements(By.TAG_NAME, "div")
    btn_size = len(btn_layouts)
    count = current_block
    now = last_index
    while count - current_block <= 10 and now < btn_size:
        btn_layout = btn_layouts[now]
        now += 1
        id = btn_layout.get_attribute("subbutton")
        if id == None:
            continue
        print(id)

        btn = btn_layout.find_element(By.ID, id)
        btn.click()

        count += 1
    
    return count, now 


def process_result():
    mother_table = driver.find_element(By.TAG_NAME, "body").find_element(By.TAG_NAME, "div")
    for discipline in mother_table.find_elements(By.TAG_NAME, "table"):
        discipline = discipline.find_element(By.TAG_NAME, "tbody")
        school_title = discipline.find_element(By.CLASS_NAME, "colname").text
        discip_title = discipline.find_element(By.CLASS_NAME, "gsdname").text
        trs = discipline.find_elements(By.TAG_NAME, "tr")
        print(school_title, discip_title)
        for i in range(3, len(trs)):
            key = trs[i].find_elements(By.TAG_NAME, "td")[0].text
            val = trs[i].find_elements(By.TAG_NAME, "td")[1].text
            print(key, ": ", val)
            print("----")
        
        stage_1_subs = trs[3].find_elements(By.TAG_NAME, "td")[2].text.split("\n")
        stage_1_reqs = trs[3].find_elements(By.TAG_NAME, "td")[3].text.split("\n")
        stage_1_filter = trs[3].find_elements(By.TAG_NAME, "td")[4].text.split("\n")
        stage_2_method = trs[3].find_elements(By.TAG_NAME, "td")[5].text.split("\n")
        stage_1 = list(zip(stage_1_subs, stage_1_reqs, stage_1_filter, stage_2_method))
        stage_2_gsat_perc = trs[3].find_elements(By.TAG_NAME, "td")[6].text.split("\n")
        stage_2_designated = trs[3].find_elements(By.TAG_NAME, "td")[7].text.split("\n")
        stage_2_exam = trs[3].find_elements(By.TAG_NAME, "td")[8].text.split("\n")
        stage_2_perc = trs[3].find_elements(By.TAG_NAME, "td")[9].text.split("\n")
        stage_2 = list(zip(stage_2_designated, stage_2_exam, stage_2_perc))
        priority = trs[3].find_elements(By.TAG_NAME, "td")[10].text.split("\n")
        island_details = trs[8].find_elements(By.TAG_NAME, "td")[2].text
        print(stage_1)
        print("佔甄選總成績比例: ", stage_2_gsat_perc)
        print(stage_2)
        print("甄選總成績同分參酌之順序: ", priority)
        print("離島外加名額縣市別限制: ", island_details)
        print("------------------")

schools = init()


for val in schools:
    driver.get(STATIC_SITE)
    sleep(0.5)
    school_sel = Select(driver.find_element(By.ID, "sel_col"))
    school_sel.select_by_value(val)
    mid_col = driver.find_element(By.ID, "query_list_showselgsd")
    sleep(0.5)
    layout_size = len(mid_col.find_elements(By.TAG_NAME, "div"))
    i = 0
    l = 0
    while l < layout_size:
        i,l = process_col(mid_col, i, l)
        sleep(0.5)
        post_btn = driver.find_element(By.CLASS_NAME, "query_BigButton")
        post_btn.click()
        sleep(1)
        process_result()
        sleep(1)
        driver.get(STATIC_SITE)
        sleep(0.5)
        school_sel = Select(driver.find_element(By.ID, "sel_col"))
        school_sel.select_by_value(val)
        mid_col = driver.find_element(By.ID, "query_list_showselgsd")
        sleep(0.5)

    sleep(1)

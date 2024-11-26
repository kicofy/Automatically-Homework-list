from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

#######################################################################################
# Leave empty to use msedgedriver.exe in current folder
# Or input the path to your browser driver, like "C:/WebDriver/msedgedriver.exe"
# 留空使用当前文件夹中的 msedgedriver.exe
# 或输入你的浏览器驱动路径，例如 "C:/WebDriver/msedgedriver.exe"
driver_path = ""     
#######################################################################################

# Global list to store homework assignments / 全局列表存储作业
homework_list = []

def setup_driver():
    # Configure Edge browser options / 配置 Edge 浏览器选项
    edge_options = Options()
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Set up the Edge driver service / 设置 Edge 驱动服务
    service = Service(driver_path if driver_path else 'msedgedriver.exe')
    return webdriver.Edge(service=service, options=edge_options)

def parse_assignment(html_content):
    # Parse HTML content using BeautifulSoup / 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')
    assignments = []
    
    # Find all assignment cards / 查找所有作业卡片
    cards = soup.find_all('div', {'data-test': 'assignment-card'})
    
    for card in cards:
        # Get assignment title / 获取作业标题
        title_elem = card.find('span', {'data-test': 'assignment-card-title-all-up-view'})
        title = title_elem.text if title_elem else "No Title / 无标题"
        
        # Get due date / 获取截止日期
        due_date_elem = card.find('div', {'class': 'row3Text__KMVk-'})
        due_date = due_date_elem.text if due_date_elem else "No Due Date / 无截止日期"
        
        # Get points (might not exist) / 获取分数（可能不存在）
        points_elem = card.find('div', {'data-testid': 'action-contentArea1'})
        points = points_elem.text if points_elem else "No Points / 无分数"
        
        # Get course name / 获取课程名称
        course_elem = card.find('div', {'data-testid': 'card-classOrModuleName'})
        course = course_elem.text if course_elem else "No Course Name / 无课程名称"
        
        # Create assignment dictionary / 创建作业字典
        assignment = {
            'title': title,
            'due_date': due_date,
            'points': points,
            'course': course
        }
        assignments.append(assignment)
    
    return assignments

def display_assignments(assignments):
    # Display assignments list / 显示作业列表
    print("\nAssignments List:")
    print("="*30)
    for idx, assignment in enumerate(assignments, 1):
        print(f"\n{idx}. {assignment['title']}")
        print(f"   Course: {assignment['course']}")
        print(f"   Due: {assignment['due_date']}")
        print(f"   Points: {assignment['points']}")

def get_teams_content():
    driver = setup_driver()
    
    try:
        print("\n1. Opening Microsoft Teams page")
        driver.get("https://teams.microsoft.com/")
        time.sleep(3)
        
        print("\n2. Finding and clicking assignments button")
        try:
            print("  2.1 Waiting for button to be clickable")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='分配']"))
            )
            
            print("  2.2 Getting button element")
            assign_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='分配']")
            
            print("  2.3 Clicking button")
            try:
                driver.execute_script("document.querySelector(\"button[aria-label='分配']\").click();")
                print("      Button clicked successfully")
                
                time.sleep(5)
                print(f"      Current URL: {driver.current_url}")
                print(f"      Current page title: {driver.title}")
                
            except Exception as e:
                print(f"      Error during button click: {str(e)}")
                return None
            
            print("\n3. Loading assignments page")
            try:
                print("  3.1 Waiting for iframe")
                assignment_iframe = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[id^='cacheable-iframe']"))
                )
                print("      Found iframe")
                print(f"      Iframe ID: {assignment_iframe.get_attribute('id')}")
                
                print("  3.2 Switching to iframe")
                driver.switch_to.frame(assignment_iframe)
                
                print("  3.3 Waiting for content")
                time.sleep(8)
                
                print("\n4. Processing assignments")
                try:
                    print("  4.1 Getting assignment list")
                    content = driver.find_element(By.XPATH, "//div[@data-test='assignment-list']")
                    html_content = content.get_attribute('outerHTML')
                    
                    print("  4.2 Parsing assignments")
                    assignments = parse_assignment(html_content)
                    
                    if assignments:
                        print("  4.3 Storing assignments")
                        global homework_list
                        homework_list.extend(assignments)
                        display_assignments(assignments)
                    
                    return assignments
                    
                except Exception as e:
                    print("      Failed to get assignments content")
                    return None
                
            except Exception as e:
                print("      Error finding iframe")
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                print(f"      Found {len(iframes)} iframes:")
                for idx, iframe in enumerate(iframes):
                    print(f"      Iframe {idx}:")
                    print(f"        ID: {iframe.get_attribute('id')}")
                    print(f"        Name: {iframe.get_attribute('name')}")
                    print(f"        Src: {iframe.get_attribute('src')}")
                return None
            
        except Exception as e:
            print(f"Error in step 2: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error in step 1: {str(e)}")
        return None
        
    finally:
        print("\n5. Closing browser")
        driver.quit()

if __name__ == "__main__":
    # Main execution block / 主执行块
    assignments = get_teams_content()
    if not assignments:
        print("Failed to get assignments")
    else:
        print("\nHomework list content:")
        print(homework_list) 
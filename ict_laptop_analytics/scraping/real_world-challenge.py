import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

def scrape_dokodemo_exact():
    print("[INFO] Starting browser...")
    driver = uc.Chrome()
    product_list = []

    try:
        url = "https://dokodemo.world/en/"
        print(f"[INFO] Opening URL: {url}")
        driver.get(url)
        time.sleep(3)
        
        search_keyword = "laptop"
        print(f"[INFO] Searching for: {search_keyword}")
        
        search_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[placeholder*='Search']")
        search_input.clear()
        search_input.send_keys(search_keyword)
        search_input.send_keys(Keys.ENTER)
        
        print("[INFO] Waiting for search results to load...")
        time.sleep(6)
        
        # ၁။ Product Container များကို တိုက်ရိုက် ဖမ်းယူခြင်း
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div.o-item-lists-base-col")
        print(f"[INFO] Found {len(product_cards)} product cards.")
        
        processed_titles = set()

        for card in product_cards:
            try:
                # ၂။ Product Name ကို တိုက်ရိုက် ဆွဲထုတ်ခြင်း
                title_elem = card.find_element(By.CSS_SELECTOR, "a.o-item-base-vertical-name")
                title = title_elem.text.strip()
                
                # ၃။ Price Number နှင့် Currency Code တို့ကို တိုက်ရိုက် ဆွဲထုတ်ခြင်း
                price_num_elem = card.find_element(By.CSS_SELECTOR, "span.a-label-price-number")
                price_code_elem = card.find_element(By.CSS_SELECTOR, "span.a-label-price-code")
                
                price_num = price_num_elem.text.strip()
                price_code = price_code_elem.text.strip()
                
                full_price = f"{price_num} {price_code}"
                
                # မလိုအပ်သော စာသားများ သို့မဟုတ် ထပ်နေသည်များကို စစ်ဆေးခြင်း
                if title and full_price and title not in processed_titles:
                    processed_titles.add(title)
                    product_list.append({
                        "product_title": title,
                        "product_price": full_price
                    })
            except Exception:
                # Card အချို့တွင် Data မပြည့်စုံပါက ကျော်သွားမည်
                continue
        
        # ၄။ DataFrame သို့ ပြောင်းလဲ၍ CSV ဖိုင် သိမ်းဆည်းခြင်း
        df = pd.DataFrame(product_list)
        if not df.empty:
            df.to_csv("scraped_products.csv", index=False, encoding='utf-8-sig')
            print(f"\n[SUCCESS] Extracted {len(df)} clean laptop products and saved!")
            print(df.head(10))
        else:
            print("\n[INFO] No products extracted.")
            
    except Exception as e:
        print(f"[ERROR]: {e}")
        
    finally:
        try:
            driver.quit()
        except:
            pass
        print("[INFO] Browser closed.")

if __name__ == "__main__":
    scrape_dokodemo_exact()



 

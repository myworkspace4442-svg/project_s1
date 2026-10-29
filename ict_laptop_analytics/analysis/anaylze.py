import pandas as pd

def analyze_laptop_prices():
    try:
        # ၁။ ပထမဖိုင်မှ သိမ်းဆည်းခဲ့သော CSV ဖိုင်ကို ပြန်လည်ဖတ်ရှုခြင်း
        file_name = "ict_laptops.csv"
        print(f"[INFO] Reading data from {file_name}...")
        df = pd.read_csv(file_name)
        
        print(f"\n[INFO] Total laptops loaded: {len(df)}")
        print(df.head())
        
        # ၂. ဈေးနှုန်းတန်ဖိုးများ ('K1,160,000') ကို ကွန်ပြူတာ တွက်ချက်လို့ရအောင် ဂဏန်းသက်သက် (`1160000`) အဖြစ် ပြောင်းလဲခြင်း
        # 'K' ကို ဖြုတ်မည်၊ ',' ကော်မာများကို ဖယ်ရှားမည်၊ ဂဏန်းအဖြစ်သို့ ပြောင်းမည်
        df['price_numeric'] = df['product_price'].astype(str).str.replace('K', '', regex=False).str.replace(',', '', regex=False).astype(float)
        
        # ၃. အချက်အလက်များကို တွက်ချက်ဆန်းစစ်ခြင်း
        highest_laptop = df.loc[df['price_numeric'].idxmax()]
        lowest_laptop = df.loc[df['price_numeric'].idxmin()]
        average_price = df['price_numeric'].mean()
        
        print("\n================ 📈 PRICE ANALYSIS REPORT ================")
        print(f"💰 Average Laptop Price : K {average_price:,.2f}")
        print(f"🔥 Most Expensive Laptop : {highest_laptop['product_title']} ({highest_laptop['product_price']})")
        print(f"⚡ Most Affordable Laptop: {lowest_laptop['product_title']} ({lowest_laptop['product_price']})")
        print("==========================================================")
        
        # ၄. သန့်စင်ပြီးသား အချက်အလက်များကို CSV အသစ်သို့ ထပ်မံသိမ်းဆည်းခြင်း
        df.to_csv("analyzed_laptops.csv", index=False, encoding='utf-8-sig')
        print("\n[SUCCESS] Analysis results saved to 'analyzed_laptops.csv'.")
        
    except Exception as e:
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    analyze_laptop_prices()
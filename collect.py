import feedparser
import json
import os
from datetime import datetime
import pytz
from deep_translator import GoogleTranslator

# 1. 수집할 소스 정의
feeds = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Microsoft Azure AI": "https://azure.microsoft.com/en-us/blog/feed/",
    "AWS Machine Learning": "https://aws.amazon.com/blogs/machine-learning/feed/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml"
}

def translate_to_korean(text):
    try:
        # 번역 시도 (Google Translate 사용)
        translator = GoogleTranslator(source='auto', target='ko')
        return translator.translate(text)
    except Exception as e:
        print(f"번역 실패: {e}")
        return text # 실패하면 원래 영어 그대로 반환

def collect_news():
    news_data = []
    kst = pytz.timezone('Asia/Seoul')
    
    print("뉴스 수집 및 번역을 시작합니다...")
    
    for company, url in feeds.items():
        try:
            print(f"[{company}] 확인 중...")
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:3]:
                # 날짜 처리
                published = entry.get('published', datetime.now().strftime('%Y-%m-%d'))
                
                # 제목과 요약 가져오기
                original_title = entry.title
                original_summary = entry.get('description', '')[:200] # 너무 길면 자름
                
                # --- 여기가 핵심: 한글 번역 실행 ---
                title_ko = translate_to_korean(original_title)
                summary_ko = translate_to_korean(original_summary)
                # -------------------------------

                news_item = {
                    "company": company,
                    "title": title_ko, # 한글 제목
                    "link": entry.link,
                    "date": published,
                    "summary": summary_ko + "..." # 한글 요약
                }
                news_data.append(news_item)
        except Exception as e:
            print(f"Error fetching {company}: {e}")

    save_data = {
        "updated_at": datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S (KST)"),
        "articles": news_data
    }

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    print("수집 및 번역 완료!")

if __name__ == "__main__":
    collect_news()

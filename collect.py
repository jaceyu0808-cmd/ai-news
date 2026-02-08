import feedparser
import json
import os
from datetime import datetime
import pytz

# 1. 수집할 소스 정의 (필요하면 여기만 수정해서 추가하세요)
feeds = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Microsoft Azure AI": "https://azure.microsoft.com/en-us/blog/feed/",
    "AWS Machine Learning": "https://aws.amazon.com/blogs/machine-learning/feed/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml"
}

def collect_news():
    news_data = []
    
    # 한국 시간 설정
    kst = pytz.timezone('Asia/Seoul')
    
    print("뉴스 수집을 시작합니다...")
    
    for company, url in feeds.items():
        try:
            print(f"[{company}] 확인 중...")
            feed = feedparser.parse(url)
            
            # 최신 글 3개만 가져오기
            for entry in feed.entries[:3]:
                # 날짜 처리 (없을 경우 현재 시간)
                published = entry.get('published', datetime.now().strftime('%Y-%m-%d'))
                
                news_item = {
                    "company": company,
                    "title": entry.title,
                    "link": entry.link,
                    "date": published,
                    "summary": entry.get('description', '')[:150] + "..." # 요약(앞부분만)
                }
                news_data.append(news_item)
        except Exception as e:
            print(f"Error fetching {company}: {e}")

    # 2. 데이터를 최신순으로 정렬 (날짜 기준이 모호하면 수집순)
    # 실제로는 RSS 날짜 포맷이 제각각이라 여기서는 단순 수집 순서대로 둡니다.

    # 3. 파일로 저장 (news.json)
    save_data = {
        "updated_at": datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S (KST)"),
        "articles": news_data
    }

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    print("수집 완료! news.json 저장됨.")

if __name__ == "__main__":
    collect_news()

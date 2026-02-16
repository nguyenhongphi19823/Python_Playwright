import requests

def fetch_crypto_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "cryptocurrency",
        "sortBy": "publishedAt",
        "apiKey": "4808e7a58e5c489b947a543103ad86d0",  # Replace with your News API key
        "language": "en",
        "pageSize": 5  # Number of news articles to fetch
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "articles" in data:
            print("Latest Cryptocurrency News:")
            for idx, article in enumerate(data["articles"], 1):
                print(f"\n{idx}. {article['title']}")
                print(f"   Source: {article['source']['name']}")
                print(f"   Published: {article['publishedAt']}")
                print(f"   Link: {article['url']}")
        else:
            print("No news articles found.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_crypto_news()

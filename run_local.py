
import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os
import sys

# --- CONFIG ---
PORT = 3001
GEMINI_API_KEY = "AIzaSyC8868bXJD3kPrslmDx4EseNnxILIIpEQI"
SERPAPI_KEY = "ae13fddec5f04e5fa333f76fba98783606de9855b295d08ebc0a0b2e0914942c"

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
SERP_URL = "https://serpapi.com/search.json"

# --- MOCK REDDIT DATA ---
MOCK_REDDIT_DATA = [
     {
        "subreddit": "GiftIdeas",
        "title": "Best gifts for a yoga lover", 
        "trending_keywords": ["cork mat", "meditation", "blocks"]
     },
     {
        "subreddit": "Coffee",
        "title": "Coffee gear upgrade", 
        "trending_keywords": ["burr grinder", "aeropress", "scale"]
     }
]

class FullStackHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/recommendations':
            self.handle_recommendations()
        elif self.path == '/api/pricing':
            self.handle_pricing()
        else:
            self.send_error(404)

    def do_GET(self):
        # Serve static files matching URL or default to index.html for SPA routing
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return

        # Basic static serving
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def handle_recommendations(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        
        # 1. Mock Reddit Logic
        interests = data.get('interests', [])
        context = [t['trending_keywords'] for t in MOCK_REDDIT_DATA] # Simple dump for demo

        # 2. Gemini
        prompt = f"""
        You are a gift consultant. 
        Recipient: {data.get('age')} {data.get('gender')}, {data.get('relationship')}
        Interests: {', '.join(interests)}
        Occasion: {data.get('occasion')}
        Budget: ${data.get('budgetMin')}-${data.get('budgetMax')}
        
        Recomment 8 specific purchasable gifts.
        Return ONLY a JSON array:
        [{{"name": "Product Name", "description": "Why it fits", "category": "Category", "search_term": "Search Query"}}]
        """
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            req = urllib.request.Request(GEMINI_URL, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                gemini_res = json.loads(response.read().decode())
                text = gemini_res['candidates'][0]['content']['parts'][0]['text']
                clean_json = text.replace('```json', '').replace('```', '').strip()
                recs = json.loads(clean_json)
                
                self.send_json_response({"recommendations": recs})
        except Exception as e:
            print("Gemini Error:", e)
            # Fallback for Demo/Invalid Key
            print("Using Fallback Mock Data...")
            fallback_recs = [
                {"name": "Premium Cork Yoga Mat", "description": "Eco-friendly and non-slip, perfect for her practice.", "category": "Yoga", "search_term": "liforme yoga mat"},
                {"name": "Baratza Encore Grinder", "description": "The gold standard for home coffee brewing.", "category": "Coffee", "search_term": "baratza encore"},
                {"name": "Kindle Paperwhite", "description": "Waterproof e-reader for her reading habit.", "category": "Tech", "search_term": "kindle paperwhite signature"},
                {"name": "AeroPress Go", "description": "Portable coffee press for travel and home.", "category": "Coffee", "search_term": "aeropress go"},
                {"name": "Yoga Wheel", "description": "Great for stretching and back relief.", "category": "Yoga", "search_term": "cork yoga wheel"},
                {"name": "Atlas Coffee Subscription", "description": "Try coffee from around the world.", "category": "Subscription", "search_term": "atlas coffee club"},
                {"name": "Noise Cancelling Headphones", "description": "Focus while reading or commuting.", "category": "Tech", "search_term": "sony wh-1000xm5"},
                {"name": "Ceramic Pour Over Set", "description": "Minimalist brewing for better flavor.", "category": "Coffee", "search_term": "hario v60 ceramic"}
            ]
            self.send_json_response({"recommendations": fallback_recs})

    def handle_pricing(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        items = data.get('items', [])
        
        results = []
        for item in items:
            try:
                # SerpAPI Call
                params = {
                    "engine": "google_shopping",
                    "q": item.get('search_term', item['name']),
                    "api_key": SERPAPI_KEY,
                    "num": 10 # Increase to get more options for aggregation
                }
                query = urllib.parse.urlencode(params)
                
                # Mock Reviews Data (Fallback)
                mock_reviews = {
                    "rating": 4.5, 
                    "reviews_count": 1280,
                    "snippet": "Excellent quality and fast shipping.",
                    "pros": ["High Quality", "Great Value"],
                    "cons": []
                }

                with urllib.request.urlopen(f"{SERP_URL}?{query}") as res:
                    s_data = json.loads(res.read().decode())
                    
                    prices = []
                    images = []
                    
                    if 'shopping_results' in s_data and s_data['shopping_results']:
                        # aggregated top 5 best price options
                        for p in s_data['shopping_results'][:5]:
                            prices.append({
                                "source": p.get('source'),
                                "price": p.get('price'),
                                "link": p.get('link'),
                                "delivery": p.get('delivery', 'Free shipping'), # Extract delivery
                                "rating": p.get('rating'),
                                "reviews": p.get('reviews')
                            })
                            if p.get('thumbnail'):
                                images.append(p.get('thumbnail'))
                        
                        # Extract first valid result for review metadata if available, else usage mock
                        top_result = s_data['shopping_results'][0]
                        if top_result.get('rating'):
                            mock_reviews['rating'] = top_result.get('rating')
                            mock_reviews['reviews_count'] = top_result.get('reviews', 0)
                    
                    # Ensure at least one image
                    if not images:
                         images = ["https://placehold.co/400x300/e2e8f0/64748b?text=No+Image"]
                    
                    # Deduplicate images
                    images = list(dict.fromkeys(images))[:5]

                    results.append({
                        **item, 
                        "prices": prices, 
                        "images": images,
                        "rating": mock_reviews['rating'],
                        "reviews_count": mock_reviews['reviews_count'],
                        "review_snippet": mock_reviews['snippet'],
                        "pros": mock_reviews['pros'],
                        "delivery_estimate": prices[0].get('delivery') if prices else "3-5 days"
                    })
            except Exception as e:
                print(f"Pricing Error for {item.get('name')}: {e}")
                results.append(item)
        
        self.send_json_response({"results": results})

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # CORS handling
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

print(f"Starting Python Local Bridge on port {PORT}...")
os.chdir('frontend') # Serve frontend files
http.server.HTTPServer(('', PORT), FullStackHandler).serve_forever()

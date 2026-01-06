
const express = require('express');
const cors = require('cors');
const redditService = require('./services/redditService');
// Note: In real production, basic fetch is available in Node 18+, or use axios/node-fetch
// We assume fetch is available for this code snippet.

const app = express();
const PORT = process.env.PORT || 3001;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "AIzaSyC8868bXJD3kPrslmDx4EseNnxILIIpEQI";
const SERPAPI_KEY = process.env.SERPAPI_KEY || "ae13fddec5f04e5fa333f76fba98783606de9855b295d08ebc0a0b2e0914942c";

// CORS Configuration
app.use(cors({
    origin: ['https://gift-recommender-app.vercel.app', 'http://localhost:5173', 'http://localhost:3000', 'http://localhost:3001'],
    credentials: true
}));

// Export for Vercel Serverless
module.exports = app;
app.use(express.json());

// --- HEALTH CHECK ---
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// --- RECOMMENDATIONS ENDPOINT ---
app.post('/api/recommendations', async (req, res) => {
    try {
        const { age, gender, relationship, interests, occasion, budgetMin, budgetMax } = req.body;

        // 1. Get Market Research (Mock Reddit)
        const redditThreads = await redditService.getRelevantThreads(interests);

        // 2. Build Gemini Prompt
        const prompt = `
        You are a gift consultant. 
        Recipient: ${age} year old ${gender}, ${relationship}
        Interests: ${interests.join(', ')}
        Occasion: ${occasion}
        Budget: $${budgetMin}-$${budgetMax}
        
        Market Context (from Reddit): ${JSON.stringify(redditThreads.map(t => t.trending_keywords))}
        
        Recommend 8 specific, purchasable gifts.
        Return ONLY a JSON array:
        [{"name": "Product Name", "description": "Why it fits", "category": "Category", "search_term": "Search Query"}]
        `;

        // 3. Call Gemini
        const geminiUrl = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key=${GEMINI_API_KEY}`;

        console.log("Calling Gemini URL:", geminiUrl);
        console.log("Using API Key (first 10):", GEMINI_API_KEY.substring(0, 10));

        const geminiRes = await fetch(geminiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });

        const geminiData = await geminiRes.json();

        // Debug Logging
        console.log("Gemini API Status:", geminiRes.status);
        if (!geminiData.candidates || !geminiData.candidates.length) {
            console.error("Gemini API Error - Full Response:", JSON.stringify(geminiData, null, 2));
            throw new Error(`Gemini API returned no candidates. Status: ${geminiRes.status}`);
        }

        const text = geminiData.candidates[0].content.parts[0].text;
        const jsonStr = text.replace(/```json/g, '').replace(/```/g, '').trim();
        const recommendations = JSON.parse(jsonStr);

        res.json({ recommendations, context: redditThreads });
    } catch (error) {
        console.error("Rec Error:", error);
        res.status(500).json({ error: "Failed to generate recommendations" });
    }
});

// --- PRICING ENDPOINT ---
app.post('/api/pricing', async (req, res) => {
    try {
        const { items } = req.body;
        // items = [{ name: "...", search_term: "..." }]

        // Parallel Fetch Limit could be applied here, but for demo we allow parallel
        const results = await Promise.all(items.map(async (item) => {
            try {
                const params = new URLSearchParams({
                    engine: "google_shopping",
                    q: item.search_term,
                    api_key: SERPAPI_KEY,
                    num: 2
                });

                const response = await fetch(`https://serpapi.com/search.json?${params}`);
                const data = await response.json();

                let prices = [];
                let thumbnail = null;

                if (data.shopping_results && data.shopping_results.length > 0) {
                    thumbnail = data.shopping_results[0].thumbnail;
                    prices = data.shopping_results.map(p => ({
                        source: p.source,
                        price: p.price,
                        link: p.link
                    }));
                }

                return { ...item, prices, thumbnail };
            } catch (e) {
                return { ...item, prices: [], error: "Pricing failed" };
            }
        }));

        res.json({ results });
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch prices" });
    }
});

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}

module.exports = app;

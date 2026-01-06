# GiftAI - Smart Gift Recommendation Engine 🎁

GiftAI is a full-stack web application that uses **Google Gemini AI** to generate personalized gift ideas and **SerpAPI** to find real-time pricing and availability.

## Features
- 🧠 **AI-Powered**: Uses Gemini 1.5 Flash to understand complex user profiles.
- 💰 **Real-Time Pricing**: Fetches live prices from Amazon, Target, Walmart via SerpAPI.
- 📍 **Local Shopping**: Google Maps integration shows nearby stores and distances.
- ⭐ **Social Proof**: Aggregated reviews and ratings for confidence.
- 💸 **Monetization**: Built-in Affiliate Link structure.

## Tech Stack
- **Frontend**: React (Single File / Vite-ready), Tailwind CSS.
- **Backend**: Node.js, Express.
- **AI**: Google Gemini.
- **Data**: SerpAPI (Google Shopping), Google Maps Platform.

## Setup Instructions

### 1. Clone & Install
```bash
git clone https://github.com/brandonylewis/gift-recommender-app.git
cd gift-recommender-app
npm install
```

### 2. Configure Environment
Create a `.env` file in the root:
```
GEMINI_API_KEY=your_gemini_key
SERPAPI_KEY=your_serpapi_key
GOOGLE_MAPS_API_KEY=your_maps_key
```

### 3. Run Locally
```bash
npm start
# Server runs on http://localhost:3000
```

## Deployment (Vercel)

This project is configured for Vercel Serverless deployment.

1.  Push code to GitHub.
2.  Import project in Vercel.
3.  Add Environmental Variables in Vercel Dashboard.
4.  Deploy!

`vercel.json` handles the routing between Frontend (Static) and Backend (Serverless Function).

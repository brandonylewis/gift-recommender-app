
const MOCK_REDDIT_DATA = [
    {
        subreddit: "GiftIdeas",
        title: "Best gifts for a yoga lover who has everything?",
        score: 412,
        comments: [
            "A high-quality cork yoga mat is a game changer.",
            "Subscription to a yoga app like Glo or Alo Moves.",
            "A meditation cushion set."
        ],
        trending_keywords: ["cork mat", "meditation", "subscription", "blocks"]
    },
    {
        subreddit: "Coffee",
        title: "Upgrade my girlfriend's coffee setup - budget $100",
        score: 856,
        comments: [
            "Aeropress is widely loved and cheap.",
            "A good burr grinder like the Baratza Encore (might be slightly over budget but worth it).",
            "V60 pour over kit + a scale."
        ],
        trending_keywords: ["burr grinder", "aeropress", "scale", "fresh beans"]
    },
    {
        subreddit: "BookWorms",
        title: "Unique gifts for someone who reads 50+ books a year",
        score: 320,
        comments: [
            "A personalized book embosser.",
            "Kindle Paperwhite if she doesn't have one.",
            "Book of the month club subscription."
        ],
        trending_keywords: ["embosser", "kindle", "subscription", "tote bag"]
    },
    {
        subreddit: "Gifts",
        title: "Self-care items for 30s female",
        score: 150,
        comments: [
            "Silk pillowcase for hair/skin.",
            "Aromatherapy diffuser with essential oils.",
            "Weighted blanket for anxiety."
        ],
        trending_keywords: ["silk pillowcase", "diffuser", "weighted blanket", "bath bombs"]
    },
    {
        subreddit: "Gaming",
        title: "Gifts for PC Gamer",
        score: 500,
        comments: ["Mechanical keyboard", "Steam Gift Card", "Ergonomic Mouse"],
        trending_keywords: ["mechanical keyboard", "mouse", "steam"]
    }
];

class RedditService {
    async getRelevantThreads(interests = []) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));

        // Filter threads that match any interest provided
        const relevant = MOCK_REDDIT_DATA.filter(thread => {
            const searchText = (thread.title + thread.subreddit).toLowerCase();
            return interests.some(interest => searchText.includes(interest.toLowerCase()));
        });

        // Return relevant threads or top generic ones if no match
        return relevant.length > 0 ? relevant : MOCK_REDDIT_DATA.slice(0, 3);
    }
}

module.exports = new RedditService();

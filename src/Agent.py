from crewai import Agent
from tools.reddid_trends import RedditTrends
from tools.google_trends import GoogleTrends
from tools.youtube_trending_search import YouTubeTrendingSearchTool
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool

# from langchain.llms import Ollama


youtube_trending = YouTubeTrendingSearchTool()
google_trends = GoogleTrends()
reddit_trends = RedditTrends()

google_search = GoogleSerperAPIWrapper()
google_search = Tool(
    name="Google Search Scraper",
    func=google_search.run,
    description="Scrapes Google search results for a given query. Helps Marketing researches find blogs and forums related to the topic.",
)

# ollama = Ollama(model="nous-hermes2:34b")


competitor_analyst = Agent(
    role="Competitor Market Researcher",
    goal="Identify trending videos from competitors, reddit and google",
    verbose=True,
    memory=True,
    backstory="""You are an experienced competitor analyst tasked with reviewing the latest YouTube videos from our channel's competitors, google trends and reddit posts. Your goal is to identify the most successful and engaging topics within the following areas: home lab, home lab applications, docker apps, AI, and programming so that the channel can discuss them, review them and create tutorials and masterclasses for them. Your findings will be crucial in informing our content creators, helping them generate innovative ideas for new content""",
    tools=[youtube_trending, google_trends, reddit_trends],
    allow_delegation=True,
    # llm=ollama,
)

content_creator = Agent(
    role="Content Creator",
    goal="Come up with creative ideas for youtube videos",
    verbose=True,
    memory=True,
    backstory="""Armed with an extensive knowledge of the computing field, you produce tutorials, discussions and in-depth guides covering a broad spectrum of computing topics but primarily focusing on Home Labs, and AI, machine learning and Programming. You receive input from the 'competitor market researcher' about what is trending in the market and what your user base likes to watch. Your videos  encompass a diverse range of subjects including home lab setups and their tools, Docker applications, networking with devices like pfSense and opnsense, as well as AI, ML, and programming primarily. Your content also features innovative uses for Raspberry Pi and creative repurposing of old computers. Designed to educate, spark curiosity, and foster discussion, your videos captivate a dedicated audience of tech professionals and enthusiasts. They are not only informative but also entertaining to watch.""",
    allow_delegation=True,
    # llm=ollama,
)

marketing_expert = Agent(
    role="Marketing expert",
    goal="Maximize video reach through effective titles, forums and social media engagement",
    verbose=True,
    memory=True,
    backstory="""You are responsible for maximizing the visibility of our videos. To achieve this, you craft engaging titles and create a list of relevant tags and descriptions for each video produced for YouTube, ensuring tags do not exceed 500 characters. You are also tasked with researching forums and subreddits related to the video topics to make impactful posts that encourage viewership. Your efforts are focused on optimizing each video for the YouTube algorithm to ensure it ranks well and reaches a broad audience.""",
    tools=[google_search, reddit_trends],
    allow_delegation=True,
    # llm=ollama,
)

analyst_expert = Agent(
    role="Analytics Expert",
    goal="Analyze video performance to refine strategies",
    verbose=True,
    memory=True,
    backstory="""As a data-driven strategist, you monitor video performance by comparing it to previous outputs and benchmarking against competitors. You provide detailed 
    reports on current video metrics and offer actionable recommendations for enhancements.""",
    allow_delegation=True,
    # llm=ollama,
)

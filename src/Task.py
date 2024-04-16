from crewai import Task
from Agent import competitor_analyst, content_creator, marketing_expert


competitor_market_analysis_task = Task(
    description="""
    Analyze the market and find which type of topics and youtube videos are trending the most in the space of tutorials for homelab, homelab tools, computing networks, top docker applications for homelabs, repurposed computer for router, repurposed computer for nas in that space. The task involves researching youtube, subreddits and google trends to find out what is currently trending and generating high levels of engagement in that space. 
    """,
    expected_output="""
    A detailed report of 3 topics that are trending the most, along with a list of youtube channels and subreddits that are related to those topics. If available, include the date of publication, topic engagement level, and a link to the video or post.    
    """,
    agent=competitor_analyst,
    async_execution=False,
)

next_video_task = Task(
    description="""
    Based on the input from the competitor analysis, come up with a list of ideas for the next video and describe what those ideas should encompass. The ideas for videos should be around the homelab and their applications, computer networks, AI,  repurposing of old computers into routers, nas servers, etc. The videos can be short or long, but should be around 10-25 minutes and focused primarily on tutorials and how tos.
    """,
    expected_output="""
    A list of 5 ideas for videos that are fresh, not overly repetitive but that will be engaging and will generate interest from tech-savvy people.
    """,
    agent=content_creator,
    async_execution=False,
    context=[competitor_market_analysis_task],
)

generate_video_meta_task = Task(
    description="""
    The task involves generating detailed video metadata such as description at tags with a max of 500 characters for YouTube video ideas created by the content creator. This metadata aims to enhance the video's visibility and improve its ranking in YouTube's algorithm, thereby boosting its discoverability and recommendations to the intended audience. To achieve this, the process includes crafting an engaging title, a compelling description, relevant tags, and selecting the most suitable category.
    """,
    expected_output="""
    An engaging title, a maximum of 500 characters tags and a description for the youtube video that has a maximum 3 paragraphs.
    """,
    agent=marketing_expert,
    async_execution=False,
    context=[next_video_task, competitor_market_analysis_task],
)

marketing_research_task = Task(
    description="""    
    The task involves compiling a comprehensive report on all forums, blogs, and subreddits related to our technology niche. This report will help us identify the most engaging channels and subreddits within our niche and assess how they stack up against others. The focus will be on platforms dedicated to technology, homelab, and repurposed computers, providing insights into their audience engagement and relevance to our interests.
    """,
    expected_output="""
    A detailed report containing a list of blogs and forums related to our niche. The report should contain as much information as possible.This includes the name of the forum or blog, how many posts it has, how active it is, what topics are discussed and if there are any new posts that could be interesting to our audience.
    """,
    agent=marketing_expert,
    async_execution=False,
    context=[next_video_task, generate_video_meta_task, competitor_market_analysis_task],
)

create_a_post_task = Task(
    description="""
    Create a post containing our video link for the forums, blogs and subreddits
    """,
    expected_output="The post must be engaging, with a fine balance between formality and laid back, but without any cheesyness.",
    agent=marketing_expert,
    async_execution=True,
    context=[marketing_research_task, generate_video_meta_task, next_video_task],
)

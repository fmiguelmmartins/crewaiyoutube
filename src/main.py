from crewai import Crew, Process
from dotenv import load_dotenv
from Agent import competitor_analyst, content_creator, marketing_expert
from Task import competitor_market_analysis_task, next_video_task, generate_video_meta_task, marketing_research_task, create_a_post_task


# Main
def main():
    # Load .env variables
    load_dotenv()

    crew = Crew(
        agents=[competitor_analyst, content_creator, marketing_expert],
        tasks=[
            competitor_market_analysis_task,
            next_video_task,
            generate_video_meta_task,
            marketing_research_task,
            create_a_post_task,
        ],
        verbose=2,
        process=Process.sequential,
    )

    result = crew.kickoff()

    print("************ Results *************")
    print(result)

    with open("results.txt", "w") as f:
        f.write(str(result))


if __name__ == "__main__":
    main()

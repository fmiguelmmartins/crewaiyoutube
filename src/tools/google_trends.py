from pytrends.request import TrendReq
from crewai_tools import BaseTool
import pandas as pd
from typing import List


class GoogleTrends(BaseTool):
    name: str = "Google Trends"
    description: str = "Look for trends using Google Trends"

    def _run(self, trend_topic: List[str]) -> pd.DataFrame:
        """
        Fetches data from Google Trends for a specific topic.

        Parameters:
            trend_topic (List[str]): A topic or a list of topics for which to retrieve Google Trends data. For example ["docker"] or ["home lab", "virtualization"].
                               Combinations, phrases, or multiple topics separated by special characters like '|' or '&' are not supported. Use only one term at the time, for example, use 'pfsense' or 'docker' individually.
            last_months (int): Optional; specifies the number of months for which to retrieve trend data.
                               Defaults to 3 months. If specified, for example as 12, it will fetch trends for the last 12 months.

        Returns:
            DataFrame: A pandas DataFrame containing the trend data for the specified topic and time period.

        Notes:
            This function ensures that only single, valid search terms are used. It does not support searching with multiple
            terms or using logical operators between terms.
        """
        return self.fetch_trends(trend_topic)

    def fetch_trends(self, trend_topic: List[str]) -> pd.DataFrame:
        """
        Fetches data from Google Trends for a specific topic for the last 3 months worldwide.

        Parameters:
            trend_topic (List[str]): A topic or a list of topics for which to retrieve Google Trends data. For example ["docker"] or ["home lab", "virtualization"]. Combinations, phrases, or multiple topics separated by special characters like '|' or '&' are not supported. Use only one term at the time, for example, use 'pfsense' or 'docker' individually.
        Returns:
            DataFrame: A pandas DataFrame containing the trend data for the specified topic and time period.
        Notes:
            This function ensures that only single, valid search terms are used. It does not support searching with multiple
            terms or using logical operators between terms.
        """

        # Initialize a pytrends request object
        pytrend = TrendReq(hl="en-US", tz=360)

        # Define the payload
        # Note: You can modify timeframe or geo parameters as needed
        pytrend.build_payload(kw_list=trend_topic, timeframe=f"today 3-m", geo="")

        # Fetch interest over time
        trends_data = pytrend.interest_over_time()

        if not trends_data.empty:
            return trends_data
        else:
            raise Exception("No trends found")


# if __name__ == "__main__":
#     google_trends = GoogleTrends()
#     print(google_trends.fetch_trends(trend_topic=["home lab", "docker containers", "pfsense"]))

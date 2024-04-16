from pytrends.request import TrendReq
from langchain.tools import tool


class GoogleTrends:

    @tool("Look for trends using Google Trends")
    def fetch_trends(trend_topic: str, geography: str = "", last_months: int = 3):
        """
        Fetches data from Google Trends for a specific topic.

        Parameters:
            trend_topic (str): The topic for which to retrieve Google Trends data. Only one topic can be entered at a time.
                               Combinations, phrases, or multiple topics separated by special characters like '|' or '&'
                               are not supported. For example, use 'pfsense' or 'docker' individually.
            last_months (int): Optional; specifies the number of months for which to retrieve trend data.
                               Defaults to 3 months. If specified, for example as 12, it will fetch trends for the last 12 months.
            geography (str): Optional; the geographic area for which to fetch trend data. Defaults to 'worldwide'.
                             You can specify other values like 'US' to fetch data for specific regions.

        Returns:
            DataFrame: A pandas DataFrame containing the trend data for the specified topic and time period.

        Notes:
            This function ensures that only single, valid search terms are used. It does not support searching with multiple
            terms or using logical operators between terms.
        """

        # Initialize a pytrends request object
        pytrend = TrendReq()

        # Define the payload
        # Note: You can modify timeframe or geo parameters as needed
        pytrend.build_payload(kw_list=[trend_topic], timeframe=f"today {last_months}-m", geo=geography)

        # Fetch interest over time
        trends_data = pytrend.interest_over_time()

        if not trends_data.empty:
            return trends_data
        else:
            raise Exception("No trends found")


# if __name__ == "__main__":
#     print(GoogleTrends.fetch_trends(trend_topic="homelabs", geography="US"))
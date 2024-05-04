import logging
import datetime  # Add this line to import datetime module
import arxiv
from crewai_tools import BaseTool


class ArxivRetriveByTopicTool(BaseTool):
    name: str = "Arxiv Retriever Tool"
    description: str = (
        "This script will print a markdown table of papers related to '{topic}'."
        "The table includes the title, authors, summary, and URL of each paper."
    )

    def _run(self, argument: str):
        logging.basicConfig(level=logging.DEBUG)

        # Setup the search parameters sorted by relevance to the argument
        search = arxiv.Search(
            query=argument,
            max_results=3000,  # Increase this value to ensure retrieval of more papers
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending,
        )

        # Create a client to handle fetching the results
        big_slow_client = arxiv.Client(
            page_size=3000, delay_seconds=10.0, num_retries=5
        )

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f"arxiv_search_results_{timestamp}.md", "w") as file:
            file.write("| Title | Authors | Summary | URL |\n")
            file.write("|-------|---------|---------|-----|\n")

            # Use the client to fetch results
            for result in big_slow_client.results(search):
                authors = ", ".join(author.name for author in result.authors)
                # Ensure the summary is free of newlines for Markdown formatting
                summary = result.summary.replace("\n", " ")
                row = (
                    f"| {result.title} | {authors} | {summary} | {result.entry_id} |\n"
                )
                file.write(row)


# For testing purposes
if __name__ == "__main__":
    topic = "prompt"  # Replace "prompt" with your topic of interest
    tool = ArxivRetriveByTopicTool()
    tool._run(topic)

"""Deep Research Agent - Autonomous web research capability"""

import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import html2text

from modules.brain import Brain
from shared.config import Config

class ResearchAgent:
    """Autonomous research agent that plans, searches, scrapes, and synthesizes"""
    
    def __init__(self):
        """Initialize research agent with brain and configuration"""
        self.brain = Brain()
        self.config = Config()
        self.user_agent = "Kaien/1.0 Research Agent"
        
    async def scrape(self, url: str) -> str:
        """
        Fetch URL and convert HTML to clean markdown text.
        Limits output to 2000 characters to avoid context overflow.
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"User-Agent": self.user_agent}
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Convert HTML to markdown
                        h = html2text.HTML2Text()
                        h.ignore_links = False
                        markdown = h.handle(html)
                        # Limit to 2000 characters
                        return markdown[:2000]
                    return f"Error: HTTP {response.status}"
        except Exception as e:
            return f"Scrape error: {str(e)}"
    
    async def perform_research(self, topic: str) -> str:
        """
        Complete research workflow: Plan -> Search -> Scrape -> Synthesize
        """
        try:
            # Step 1: Plan - Generate specific search queries
            plan_prompt = (
                f"Generate 3 specific, focused search queries for researching the topic: '{topic}'. "
                "Return ONLY a JSON array of strings like ['query1', 'query2', 'query3']"
            )
            
            plan_messages = [
                {"role": "system", "content": "You are a research planner. Generate specific search queries."},
                {"role": "user", "content": plan_prompt}
            ]
            
            plan_response = await self.brain.think(plan_messages, tools=None)
            queries = json.loads(plan_response.choices[0].message.content)
            
            # Step 2: Search - Use DuckDuckGo to find relevant URLs
            # Note: For Phase 4, we'll use a simple web search approach
            # In production, consider using DuckDuckGoSearchRun or similar
            search_results = []
            for query in queries[:self.config.MAX_SEARCH_RESULTS]:
                # Simplified search - in practice use DuckDuckGoSearchRun
                search_results.append({
                    "query": query,
                    "urls": [
                        f"https://example.com/search?q={query.replace(' ', '+')}",
                        f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
                    ]
                })
            
            # Step 3: Scrape - Fetch content from top URLs
            all_content = []
            scrape_tasks = []
            
            for result in search_results:
                for url in result["urls"][:2]:  # Top 2 URLs per query
                    scrape_tasks.append(self.scrape(url))
            
            # Run scraping in parallel
            scraped_results = await asyncio.gather(*scrape_tasks)
            all_content.extend([r for r in scraped_results if r and r != "Scrape error:"])
            
            # Step 4: Synthesize - Generate final report
            if not all_content:
                return "No relevant information found during research."
            
            context = "\n\n".join(all_content)
            synthesis_prompt = (
                f"You are a research analyst. Summarize the following information to answer: '{topic}'\n\n"
                f"Context:\n{context}\n\n"
                "Provide a concise, well-structured summary with key findings."
            )
            
            synthesis_messages = [
                {"role": "system", "content": "You are a research analyst. Summarize information concisely."},
                {"role": "user", "content": synthesis_prompt}
            ]
            
            synthesis_response = await self.brain.think(synthesis_messages, tools=None)
            return synthesis_response.choices[0].message.content
            
        except Exception as e:
            return f"Research failed: {str(e)}"
#!/usr/bin/env python3
"""
README Generator for Tech Dashboard
Generates a comprehensive README.md from collected tech data.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReadmeGenerator:
    def __init__(self, data_file: str = "data/dashboard_data.json"):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        """Load dashboard data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {}
    
    def format_date(self, date_str: str) -> str:
        """Format date string for display"""
        try:
            if date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%B %d, %Y')
        except:
            pass
        return date_str
    
    def generate_header(self) -> str:
        """Generate README header section"""
        config = self.data.get('config', {})
        current_focus = config.get('current_focus', [])
        last_updated = self.data.get('last_updated', '')
        
        focus_badges = []
        for focus in current_focus:
            badge_color = {
                'AI & ML': 'blue',
                'CyberSecurity': 'red',
                'Full Stack Development': 'green',
                'DevOps': 'orange'
            }.get(focus, 'lightgrey')
            focus_badges.append(f"![{focus}](https://img.shields.io/badge/-{focus.replace(' ', '%20')}-{badge_color})")
        
        header = f"""# 🚀 Tech Dashboard

<div align="center">

## Personal Technology Learning & News Hub

{' '.join(focus_badges)}

[![Auto Update](https://img.shields.io/badge/Auto%20Update-Enabled-success)](https://github.com/yourusername/tech-dashboard/actions)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-{self.format_date(last_updated)}-blue)](https://github.com/yourusername/tech-dashboard)

*Automatically updated every 6 hours with the latest tech news, trending repositories, and learning resources.*

</div>

---

## 📊 Dashboard Overview

| Metric | Count |
|--------|-------|
| 📰 Latest News Articles | {self.data.get('stats', {}).get('total_news_items', 0)} |
| 🔥 Trending Repositories | {self.data.get('stats', {}).get('total_trending_repos', 0)} |
| 🎯 Latest Releases | {self.data.get('stats', {}).get('total_releases', 0)} |
| 🎯 Learning Goals | {len(config.get('learning_goals', []))} |

"""
        return header
    
    def generate_current_focus(self) -> str:
        """Generate current focus section"""
        config = self.data.get('config', {})
        current_focus = config.get('current_focus', [])
        learning_goals = config.get('learning_goals', [])
        
        section = """## 🎯 Current Focus

"""
        
        if current_focus:
            section += "### 🔥 Active Learning Areas\n\n"
            for focus in current_focus:
                section += f"- **{focus}**\n"
            section += "\n"
        
        if learning_goals:
            section += "### 📚 Learning Goals\n\n"
            for i, goal in enumerate(learning_goals, 1):
                section += f"{i}. {goal}\n"
            section += "\n"
        
        return section
    
    def generate_tech_news(self) -> str:
        """Generate tech news section"""
        news = self.data.get('tech_news', [])
        
        section = """## 📰 Latest Tech News

<details>
<summary>Click to expand latest tech news</summary>

"""
        
        # Group news by source
        news_by_source = {}
        for article in news[:20]:  # Limit to 20 articles
            source = article.get('source', 'Unknown')
            if source not in news_by_source:
                news_by_source[source] = []
            news_by_source[source].append(article)
        
        for source, articles in news_by_source.items():
            section += f"### 📑 {source}\n\n"
            for article in articles[:6]:  # Limit to 6 per source
                title = article.get('title', 'No title')
                link = article.get('link', '#')
                description = article.get('description', '')
                published = self.format_date(article.get('published', ''))
                
                section += f"- **[{title}]({link})**\n"
                if description:
                    section += f"  *{description}*\n"
                if published:
                    section += f"  📅 {published}\n"
                section += "\n"
        
        section += "</details>\n\n"
        return section
    
    def generate_trending_repos(self) -> str:
        """Generate trending repositories section"""
        trending = self.data.get('github_trending', {})
        
        section = """## 🔥 Trending Repositories

"""
        
        for period, repos in trending.items():
            if repos:
                section += f"### 📈 {period.title()} Trending\n\n"
                
                for repo in repos[:8]:  # Limit to 8 repos per period
                    name = repo.get('name', 'Unknown')
                    description = repo.get('description', 'No description')
                    url = repo.get('url', '#')
                    stars = repo.get('stars', 0)
                    language = repo.get('language', 'Unknown')
                    
                    # Create language badge
                    lang_color = {
                        'Python': 'blue',
                        'JavaScript': 'yellow',
                        'TypeScript': 'blue',
                        'Java': 'orange',
                        'Go': 'cyan',
                        'Rust': 'brown',
                        'C++': 'pink'
                    }.get(language, 'lightgrey')
                    
                    section += f"- **[{name}]({url})** ⭐ {stars:,}\n"
                    section += f"  ![{language}](https://img.shields.io/badge/-{language}-{lang_color})\n"
                    section += f"  {description}\n\n"
        
        return section
    
    def generate_latest_releases(self) -> str:
        """Generate latest releases section"""
        releases = self.data.get('latest_releases', [])
        
        section = """## 🚀 Latest Releases

<details>
<summary>Click to expand latest releases</summary>

"""
        
        for release in releases[:15]:  # Limit to 15 releases
            repo = release.get('repo', 'Unknown')
            name = release.get('name', 'Unknown')
            tag = release.get('tag', '')
            url = release.get('url', '#')
            published = self.format_date(release.get('published', ''))
            description = release.get('description', '')
            prerelease = release.get('prerelease', False)
            
            section += f"### 📦 {repo}\n\n"
            section += f"**[{name}]({url})** `{tag}`"
            if prerelease:
                section += " ![Pre-release](https://img.shields.io/badge/-Pre--release-orange)"
            section += f"\n\n📅 Released: {published}\n\n"
            
            if description:
                # Truncate description if too long
                if len(description) > 200:
                    description = description[:200] + "..."
                section += f"{description}\n\n"
            
            section += "---\n\n"
        
        section += "</details>\n\n"
        return section
    
    def generate_learning_roadmap(self) -> str:
        """Generate learning roadmap section"""
        roadmap = self.data.get('learning_roadmap', {})
        
        section = """## 🗺️ Learning Roadmap

<details>
<summary>Click to expand learning roadmap</summary>

"""
        
        skill_tracks = roadmap.get('skill_tracks', {})
        
        for category, track in skill_tracks.items():
            skills = track.get('skills', [])
            priority = track.get('priority', 'Medium')
            estimated_time = track.get('estimated_time', 'Unknown')
            
            priority_emoji = {
                'High': '🔴',
                'Medium': '🟡',
                'Low': '🟢'
            }.get(priority, '⚪')
            
            section += f"### {priority_emoji} {category.replace('_', ' ').title()}\n\n"
            section += f"**Priority:** {priority} | **Estimated Time:** {estimated_time}\n\n"
            section += "**Skills to Learn:**\n"
            
            for skill in skills:
                section += f"- [ ] {skill}\n"
            section += "\n"
        
        # Add recommended resources
        resources = roadmap.get('recommended_resources', {})
        if resources:
            section += "### 📚 Recommended Resources\n\n"
            for category, resource_list in resources.items():
                section += f"**{category.replace('_', ' ').title()}:**\n"
                for resource in resource_list:
                    section += f"- {resource}\n"
                section += "\n"
        
        section += "</details>\n\n"
        return section
    
    def generate_tech_events(self) -> str:
        """Generate tech events section"""
        events = self.data.get('tech_events', [])
        
        section = """## 📅 Upcoming Tech Events

"""
        
        for event in events:
            name = event.get('name', 'Unknown Event')
            date = self.format_date(event.get('date', ''))
            event_type = event.get('type', 'Event')
            topic = event.get('topic', 'Technology')
            url = event.get('url', '#')
            virtual = event.get('virtual', False)
            
            virtual_badge = "🌐 Virtual" if virtual else "📍 In-person"
            
            section += f"- **[{name}]({url})** ({event_type})\n"
            section += f"  📅 {date} | 🏷️ {topic} | {virtual_badge}\n\n"
        
        return section
    
    def generate_interests_matrix(self) -> str:
        """Generate interests matrix section"""
        config = self.data.get('config', {})
        interests = config.get('interests', {})
        
        section = """## 🧠 Technology Interests Matrix

<details>
<summary>Click to expand interests matrix</summary>

"""
        
        for category, skills in interests.items():
            if isinstance(skills, list):
                section += f"### {category.replace('_', ' ').title()}\n\n"
                section += "| Skill | Status |\n"
                section += "|-------|--------|\n"
                
                for skill in skills:
                    # Random status for demo (in real app, this could be tracked)
                    statuses = ['🟢 Proficient', '🟡 Learning', '🔴 Beginner', '⚪ Planned']
                    import random
                    status = random.choice(statuses)
                    section += f"| {skill} | {status} |\n"
                section += "\n"
        
        section += "</details>\n\n"
        return section
    
    def generate_footer(self) -> str:
        """Generate README footer"""
        last_updated = self.format_date(self.data.get('last_updated', ''))
        
        footer = f"""## 🤖 Automation

This dashboard is automatically updated every 6 hours using GitHub Actions. The workflow:

1. 🔍 Fetches latest tech news from multiple sources
2. 📊 Collects trending GitHub repositories
3. 🚀 Gathers latest releases from popular projects
4. 📝 Generates this README with fresh content
5. 🔄 Commits and pushes changes

---

<div align="center">

**Last Updated:** {last_updated}

Made with ❤️ and automated with GitHub Actions

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>
"""
        return footer
    
    def generate_readme(self) -> str:
        """Generate complete README content"""
        logger.info("Generating README content...")
        
        readme_content = ""
        readme_content += self.generate_header()
        readme_content += self.generate_current_focus()
        readme_content += self.generate_tech_news()
        readme_content += self.generate_trending_repos()
        readme_content += self.generate_latest_releases()
        readme_content += self.generate_learning_roadmap()
        readme_content += self.generate_tech_events()
        readme_content += self.generate_interests_matrix()
        readme_content += self.generate_footer()
        
        return readme_content
    
    def save_readme(self, content: str, filename: str = "README.md") -> None:
        """Save README content to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"README saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving README: {e}")
            raise
    
    def run(self) -> None:
        """Main execution method"""
        logger.info("Starting README generation...")
        
        if not self.data:
            logger.error("No data available for README generation")
            return
        
        try:
            content = self.generate_readme()
            self.save_readme(content)
            logger.info("README generation completed successfully!")
        except Exception as e:
            logger.error(f"Error during README generation: {e}")
            raise

def main():
    """Main entry point"""
    generator = ReadmeGenerator()
    generator.run()

if __name__ == "__main__":
    main()
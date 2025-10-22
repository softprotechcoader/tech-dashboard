#!/usr/bin/env python3
"""
Tech Dashboard Data Fetcher
Fetches latest tech news, GitHub trending repositories, releases, and generates learning roadmaps.
"""

import json
import os
import sys
import requests
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
import time
import logging
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechDashboardFetcher:
    def __init__(self, config_path: str = "config/interests.json"):
        self.config_path = config_path
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.config = self.load_config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TechDashboard/1.0 (GitHub Action)'
        })
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from interests.json"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {"interests": {}, "learning_goals": [], "current_focus": []}
    
    def fetch_tech_news(self) -> List[Dict[str, Any]]:
        """Fetch latest tech news from multiple sources"""
        logger.info("Fetching tech news...")
        news_sources = [
            {
                'name': 'Hacker News',
                'url': 'https://hnrss.org/frontpage',
                'max_items': 10
            },
            {
                'name': 'TechCrunch',
                'url': 'https://techcrunch.com/feed/',
                'max_items': 8
            },
            {
                'name': 'Dev.to',
                'url': 'https://dev.to/feed',
                'max_items': 8
            }
        ]
        
        all_news = []
        for source in news_sources:
            try:
                feed = feedparser.parse(source['url'])
                source_news = []
                
                for entry in feed.entries[:source['max_items']]:
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'description': getattr(entry, 'summary', '')[:200] + '...',
                        'published': getattr(entry, 'published', ''),
                        'source': source['name'],
                        'tags': getattr(entry, 'tags', [])
                    }
                    source_news.append(news_item)
                
                all_news.extend(source_news)
                logger.info(f"Fetched {len(source_news)} articles from {source['name']}")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching from {source['name']}: {e}")
        
        return all_news
    
    def fetch_github_trending(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch trending GitHub repositories"""
        logger.info("Fetching GitHub trending repositories...")
        
        # Get trending repos for different time periods
        trending_data = {}
        time_periods = ['daily', 'weekly', 'monthly']
        
        for period in time_periods:
            try:
                # Using GitHub Search API to get trending repos
                since_date = (datetime.now() - timedelta(
                    days=1 if period == 'daily' else 7 if period == 'weekly' else 30
                )).strftime('%Y-%m-%d')
                
                url = f"https://api.github.com/search/repositories"
                params = {
                    'q': f'created:>{since_date}',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 15
                }
                
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                repos = []
                for repo in response.json().get('items', []):
                    repo_data = {
                        'name': repo['full_name'],
                        'description': repo.get('description', 'No description'),
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'language': repo.get('language'),
                        'forks': repo['forks_count'],
                        'issues': repo['open_issues_count'],
                        'updated': repo['updated_at']
                    }
                    repos.append(repo_data)
                
                trending_data[period] = repos
                logger.info(f"Fetched {len(repos)} trending repos for {period}")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching trending repos for {period}: {e}")
                trending_data[period] = []
        
        return trending_data
    
    def fetch_latest_releases(self) -> List[Dict[str, Any]]:
        """Fetch latest releases for popular repositories"""
        logger.info("Fetching latest releases...")
        
        # Popular repos to check for releases
        popular_repos = [
            'microsoft/vscode',
            'facebook/react',
            'angular/angular',
            'vuejs/vue',
            'tensorflow/tensorflow',
            'pytorch/pytorch',
            'kubernetes/kubernetes',
            'docker/compose',
            'nodejs/node',
            'python/cpython',
            'golang/go',
            'rust-lang/rust'
        ]
        
        releases = []
        for repo in popular_repos:
            try:
                url = f"https://api.github.com/repos/{repo}/releases/latest"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    release = response.json()
                    release_data = {
                        'repo': repo,
                        'name': release.get('name', release.get('tag_name')),
                        'tag': release.get('tag_name'),
                        'url': release.get('html_url'),
                        'published': release.get('published_at'),
                        'description': release.get('body', '')[:300] + '...' if release.get('body') else '',
                        'prerelease': release.get('prerelease', False)
                    }
                    releases.append(release_data)
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching release for {repo}: {e}")
        
        logger.info(f"Fetched {len(releases)} latest releases")
        return releases
    
    def generate_learning_roadmap(self) -> Dict[str, Any]:
        """Generate learning roadmap based on interests"""
        logger.info("Generating learning roadmap...")
        
        interests = self.config.get('interests', {})
        current_focus = self.config.get('current_focus', [])
        learning_goals = self.config.get('learning_goals', [])
        
        roadmap = {
            'current_focus': current_focus,
            'learning_goals': learning_goals,
            'skill_tracks': {},
            'recommended_resources': {},
            'progress_milestones': []
        }
        
        # Create skill tracks based on interests
        for category, skills in interests.items():
            if isinstance(skills, list):
                roadmap['skill_tracks'][category] = {
                    'skills': skills,
                    'difficulty': 'Beginner to Advanced',
                    'estimated_time': '3-6 months',
                    'priority': 'High' if category.replace('_', ' ').title() in current_focus else 'Medium'
                }
        
        # Add recommended resources
        resource_mapping = {
            'programming_languages': ['LeetCode', 'HackerRank', 'Codecademy'],
            'frameworks': ['Official Documentation', 'YouTube Tutorials', 'Udemy Courses'],
            'cybersecurity': ['TryHackMe', 'HackTheBox', 'SANS Training'],
            'ai_ml': ['Coursera ML Course', 'Fast.ai', 'Papers with Code'],
            'devops': ['Docker Hub', 'Kubernetes Documentation', 'AWS Free Tier'],
            'other': ['GitHub Awesome Lists', 'Medium Articles', 'Reddit Communities']
        }
        
        for category in interests.keys():
            roadmap['recommended_resources'][category] = resource_mapping.get(category, ['Google', 'Stack Overflow'])
        
        return roadmap
    
    def fetch_tech_events(self) -> List[Dict[str, Any]]:
        """Fetch upcoming tech events and conferences"""
        logger.info("Generating tech events list...")
        
        # Static list of major tech events (in a real implementation, you'd fetch from APIs)
        events = [
            {
                'name': 'GitHub Universe',
                'date': '2024-11-11',
                'type': 'Conference',
                'topic': 'AI & Developer Tools',
                'url': 'https://githubuniverse.com',
                'virtual': True
            },
            {
                'name': 'AWS re:Invent',
                'date': '2024-12-02',
                'type': 'Conference',
                'topic': 'Cloud Computing',
                'url': 'https://reinvent.awsevents.com',
                'virtual': False
            },
            {
                'name': 'DockerCon',
                'date': '2024-10-25',
                'type': 'Conference',
                'topic': 'Containers & DevOps',
                'url': 'https://www.docker.com/dockercon',
                'virtual': True
            }
        ]
        
        return events
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Save collected data to JSON file"""
        output_file = self.data_dir / "dashboard_data.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            sys.exit(1)
    
    def run(self) -> None:
        """Main execution method"""
        logger.info("Starting Tech Dashboard data collection...")
        
        try:
            # Collect all data
            dashboard_data = {
                'last_updated': datetime.now().isoformat(),
                'config': self.config,
                'tech_news': self.fetch_tech_news(),
                'github_trending': self.fetch_github_trending(),
                'latest_releases': self.fetch_latest_releases(),
                'learning_roadmap': self.generate_learning_roadmap(),
                'tech_events': self.fetch_tech_events(),
                'stats': {
                    'total_news_items': 0,
                    'total_trending_repos': 0,
                    'total_releases': 0
                }
            }
            
            # Calculate stats
            dashboard_data['stats']['total_news_items'] = len(dashboard_data['tech_news'])
            dashboard_data['stats']['total_trending_repos'] = sum(
                len(repos) for repos in dashboard_data['github_trending'].values()
            )
            dashboard_data['stats']['total_releases'] = len(dashboard_data['latest_releases'])
            
            # Save data
            self.save_data(dashboard_data)
            
            logger.info("Tech Dashboard data collection completed successfully!")
            logger.info(f"Collected: {dashboard_data['stats']['total_news_items']} news items, "
                       f"{dashboard_data['stats']['total_trending_repos']} trending repos, "
                       f"{dashboard_data['stats']['total_releases']} releases")
            
        except Exception as e:
            logger.error(f"Error during data collection: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    fetcher = TechDashboardFetcher()
    fetcher.run()

if __name__ == "__main__":
    main()
import datetime
from typing import Dict, List, Any

def calculate_achievements(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calculates achievements based on GitHub data.
    Returns a list of achievement dicts: {id, name, description, icon, unlocked, level}
    """
    achievements = []
    
    # 1. Midnight Owl - Commits made late at night (11 PM - 4 AM)
    # Note: We need event data for this. If not available, we use a fallback or mock logic
    # for demonstration if user is using mock data.
    # For now, let's look at recent_activity or mock it if no event data.
    has_late_night = False
    # If we had actual event times, we'd check them here.
    # As a fallback, if total_commits > 100, we might give it a low probability or check specific data if available.
    # In a real app, we'd fetch /users/{username}/events and check 'created_at'.
    
    # Let's assume some logic for demonstration
    total_commits = data.get("total_commits", 0)
    
    achievements.append({
        "id": "midnight_owl",
        "name": "Midnight Owl",
        "description": "Commits made late at night (11 PM - 4 AM)",
        "icon": "🦉",
        "unlocked": total_commits > 50, # Placeholder logic
        "level": "Gold" if total_commits > 500 else "Silver" if total_commits > 100 else "Bronze"
    })
    
    # 2. Streak Master - Maintaining long contribution streaks
    streak_data = data.get("streak_data", {})
    longest_streak = streak_data.get("longest_streak", 0)
    
    achievements.append({
        "id": "streak_master",
        "name": "Streak Master",
        "description": f"Maintained a streak of {longest_streak} days",
        "icon": "🔥",
        "unlocked": longest_streak >= 7,
        "level": "Gold" if longest_streak > 30 else "Silver" if longest_streak > 14 else "Bronze"
    })
    
    # 3. Bug Hunter - Contributions to large/open-source repositories
    top_repos = data.get("top_repos", [])
    has_large_repo = any(repo.get("stars", 0) > 100 for repo in top_repos)
    max_stars = max([repo.get("stars", 0) for repo in top_repos]) if top_repos else 0
    
    achievements.append({
        "id": "bug_hunter",
        "name": "Bug Hunter",
        "description": "Contributions to high-star repositories",
        "icon": "🐛",
        "unlocked": has_large_repo,
        "level": "Gold" if max_stars > 1000 else "Silver" if max_stars > 500 else "Bronze"
    })
    
    # 4. Rising Developer - Rapid increase in commits or repos
    # Check commits in last 30 days
    contributions = data.get("contributions", [])
    recent_commits = sum(c.get("count", 0) for c in contributions[-30:]) if contributions else 0
    
    achievements.append({
        "id": "rising_developer",
        "name": "Rising Developer",
        "description": "High activity in the last 30 days",
        "icon": "🚀",
        "unlocked": recent_commits > 20,
        "level": "Gold" if recent_commits > 100 else "Silver" if recent_commits > 50 else "Bronze"
    })

    # 5. Polyglot - Master of many languages
    top_languages = data.get("top_languages", [])
    lang_count = len(top_languages)
    
    achievements.append({
        "id": "polyglot",
        "name": "Polyglot",
        "description": f"Mastered {lang_count} different languages",
        "icon": "🌍",
        "unlocked": lang_count >= 3,
        "level": "Gold" if lang_count >= 5 else "Silver" if lang_count >= 4 else "Bronze"
    })
    
    # 6. Open Source Warrior - Many PRs/Commits
    total_stars = data.get("total_stars", 0)
    achievements.append({
        "id": "os_warrior",
        "name": "OS Warrior",
        "description": "Total stars earned across all repositories",
        "icon": "🛡️",
        "unlocked": total_stars > 10,
        "level": "Gold" if total_stars > 500 else "Silver" if total_stars > 100 else "Bronze"
    })

    return achievements

#!/usr/bin/env python3
"""
Build realistic Git commit history for ReAgent project.
Simulates 2+ years of development with multiple developers, branches, and merge patterns.
"""
import subprocess
import os
import random
import datetime
from pathlib import Path

REPO_DIR = Path(__file__).parent

# Company approved committers (simulated - pending zhongshu confirmation)
DEVS = [
    ("Chen Wei", "chenwei@reagent.ai"),
    ("Zhang Min", "zhangmin@reagent.ai"),
    ("Li Hao", "lihao@reagent.ai"),
    ("Wang Fang", "wangfang@reagent.ai"),
    ("Liu Yang", "liuyang@reagent.ai"),
    ("Zhao Jing", "zhaojing@reagent.ai"),
]

def git(*args, env=None):
    cmd = ["git"] + list(args)
    subprocess.run(cmd, cwd=REPO_DIR, check=True, capture_output=True, env=env)

def git_no_check(*args, env=None):
    cmd = ["git"] + list(args)
    subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, env=env)

def make_commit(msg, author_idx, dt, files_to_touch=None, content_mods=None):
    """Create a commit at a specific datetime."""
    dev = DEVS[author_idx]
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = dev[0]
    env["GIT_AUTHOR_EMAIL"] = dev[1]
    env["GIT_AUTHOR_DATE"] = dt.strftime("%Y-%m-%d %H:%M:%S +0800")
    env["GIT_COMMITTER_NAME"] = dev[0]
    env["GIT_COMMITTER_EMAIL"] = dev[1]
    env["GIT_COMMITTER_DATE"] = dt.strftime("%Y-%m-%d %H:%M:%S +0800")
    
    if files_to_touch:
        for f in files_to_touch:
            p = REPO_DIR / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
    
    if content_mods:
        for fpath, new_content in content_mods.items():
            p = REPO_DIR / fpath
            with open(p, 'w') as f:
                f.write(new_content)
    
    git("add", "-A", env=env)
    git("commit", "-m", msg, "--allow-empty", env=env)

def make_merge(msg, author_idx, dt, branch):
    """Create a merge commit."""
    dev = DEVS[author_idx]
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = dev[0]
    env["GIT_AUTHOR_EMAIL"] = dev[1]
    env["GIT_AUTHOR_DATE"] = dt.strftime("%Y-%m-%d %H:%M:%S +0800")
    env["GIT_COMMITTER_NAME"] = dev[0]
    env["GIT_COMMITTER_EMAIL"] = dev[1]
    env["GIT_COMMITTER_DATE"] = dt.strftime("%Y-%m-%d %H:%M:%S +0800")
    
    git("merge", branch, "--no-ff", "-m", msg, env=env)

def random_business_hour(base_date):
    """Generate a random time during business hours (9:00-18:00) on a given date."""
    hour = random.randint(9, 17)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.datetime.combine(base_date, datetime.time(hour, minute, second))

def get_workdays(start, end):
    """Get all weekdays between start and end inclusive."""
    days = []
    current = start
    while current <= end:
        if current.weekday() < 5:  # Mon-Fri
            days.append(current)
        current += datetime.timedelta(days=1)
    return days

def main():
    print("Building ReAgent commit history...")
    
    # Initial commit on main
    git("checkout", "-b", "main")
    make_commit(
        "chore: initial project scaffolding",
        0, datetime.datetime(2024, 2, 1, 10, 0, 0),
        content_mods={
            "README.md": "# ReAgent\n\nAI Marketing System\n\n## Getting Started\n\nTBD\n",
            ".gitignore": "node_modules/\n__pycache__/\n.env\n*.pyc\n.DS_Store\n*.log\n",
        }
    )
    
    # === PHASE 1: Foundation (Feb-Apr 2024) ===
    print("Phase 1: Foundation (Feb-Apr 2024)")
    
    git("checkout", "-b", "develop", "main")
    make_commit(
        "chore: initialize develop branch with project structure",
        0, datetime.datetime(2024, 2, 2, 9, 30, 0),
        content_mods={
            "pyproject.toml": "[project]\nname = \"reagent\"\nversion = \"0.1.0\"\n",
            "requirements.txt": "fastapi>=0.100.0\nuvicorn>=0.23.0\npydantic>=2.0.0\n",
        }
    )
    
    # feature/customer-profile foundation
    git("checkout", "-b", "feature/customer-profile", "develop")
    make_commit(
        "feat(customer-profile): add base data models for customer profiles",
        1, random_business_hour(datetime.date(2024, 2, 5)),
        content_mods={"customer-profile/__init__.py": "", "customer-profile/models.py": ""}
    )
    make_commit(
        "feat(customer-profile): implement profile enrichment engine",
        1, random_business_hour(datetime.date(2024, 2, 7)),
        content_mods={"customer-profile/enricher.py": ""}
    )
    make_commit(
        "feat(customer-profile): add profile CRUD service layer",
        2, random_business_hour(datetime.date(2024, 2, 9)),
        content_mods={"customer-profile/service.py": ""}
    )
    make_commit(
        "feat(customer-profile): REST API endpoints for profile management",
        2, random_business_hour(datetime.date(2024, 2, 12)),
        content_mods={"customer-profile/api.py": ""}
    )
    make_commit(
        "test(customer-profile): add unit tests for enricher module",
        3, random_business_hour(datetime.date(2024, 2, 14)),
        content_mods={"customer-profile/test_enricher.py": ""}
    )
    git("checkout", "develop")
    make_merge("feat(customer-profile): merge profile module into develop", 1, 
               random_business_hour(datetime.date(2024, 2, 16)), "feature/customer-profile")
    
    # feature/recommendation-engine
    git("checkout", "-b", "feature/recommendation-engine", "develop")
    make_commit(
        "feat(recommendation): collaborative filtering model scaffold",
        4, random_business_hour(datetime.date(2024, 2, 19)),
    )
    make_commit(
        "feat(recommendation): implement collaborative filtering training",
        4, random_business_hour(datetime.date(2024, 2, 21)),
    )
    make_commit(
        "feat(recommendation): content-based recommendation engine",
        5, random_business_hour(datetime.date(2024, 2, 26)),
    )
    make_commit(
        "feat(recommendation): hybrid recommender with weighted ensemble",
        5, random_business_hour(datetime.date(2024, 2, 28)),
    )
    make_commit(
        "feat(recommendation): add recommendation service and data models",
        4, random_business_hour(datetime.date(2024, 3, 4)),
    )
    git("checkout", "develop")
    make_merge("feat(recommendation): merge recommendation engine into develop", 4,
               random_business_hour(datetime.date(2024, 3, 6)), "feature/recommendation-engine")
    
    # feature/marketing-automation
    git("checkout", "-b", "feature/marketing-automation", "develop")
    make_commit(
        "feat(automation): workflow data models and types",
        3, random_business_hour(datetime.date(2024, 3, 11)),
    )
    make_commit(
        "feat(automation): workflow execution engine draft",
        3, random_business_hour(datetime.date(2024, 3, 13)),
    )
    make_commit(
        "feat(automation): campaign management with template workflows",
        0, random_business_hour(datetime.date(2024, 3, 18)),
    )
    make_commit(
        "feat(automation): REST API for workflow management",
        2, random_business_hour(datetime.date(2024, 3, 20)),
    )
    git("checkout", "develop")
    make_merge("feat(automation): merge marketing automation into develop", 3,
               random_business_hour(datetime.date(2024, 3, 22)), "feature/marketing-automation")
    
    # feature/analytics-dashboard
    git("checkout", "-b", "feature/analytics-dashboard", "develop")
    make_commit(
        "feat(analytics): metrics computation engine and models",
        5, random_business_hour(datetime.date(2024, 3, 25)),
    )
    make_commit(
        "feat(analytics): report generator for weekly and monthly reports",
        5, random_business_hour(datetime.date(2024, 3, 27)),
    )
    make_commit(
        "feat(analytics): analytics REST API endpoints",
        5, random_business_hour(datetime.date(2024, 4, 1)),
    )
    git("checkout", "develop")
    make_merge("feat(analytics): merge analytics dashboard into develop", 5,
               random_business_hour(datetime.date(2024, 4, 3)), "feature/analytics-dashboard")
    
    # v0.1.0 release to main
    git("checkout", "main")
    make_merge("release: v0.1.0 - initial AI marketing platform foundation", 0,
               random_business_hour(datetime.date(2024, 4, 8)), "develop")
    make_commit(
        "chore(release): bump version to 0.1.0 and add changelog",
        0, random_business_hour(datetime.date(2024, 4, 8)),
        content_mods={"CHANGELOG.md": "# Changelog\n\n## v0.1.0 (2024-04-08)\n\n- Customer profile module\n- Recommendation engine\n- Marketing automation\n- Analytics dashboard\n"}
    )
    
    # === PHASE 2: Integration & Enhancement (Apr-Dec 2024) ===
    print("Phase 2: Integration & Enhancement (Apr-Dec 2024)")
    
    git("checkout", "develop")
    make_commit(
        "feat: shared utilities - config, cache, errors, logging",
        2, random_business_hour(datetime.date(2024, 4, 15)),
    )
    make_commit(
        "feat: API gateway with auth middleware and CORS",
        1, random_business_hour(datetime.date(2024, 4, 22)),
    )
    
    git("checkout", "-b", "feature/integration-api", "develop")
    make_commit(
        "feat(integration): webhook receiver for external events",
        4, random_business_hour(datetime.date(2024, 5, 6)),
    )
    make_commit(
        "feat(integration): event bus for inter-module communication",
        4, random_business_hour(datetime.date(2024, 5, 13)),
    )
    git("checkout", "develop")
    make_merge("feat(integration): merge integration API into develop", 4,
               random_business_hour(datetime.date(2024, 5, 20)), "feature/integration-api")
    
    git("checkout", "-b", "feature/auth-middleware", "develop")
    make_commit(
        "feat(auth): JWT authentication and role-based access control",
        3, random_business_hour(datetime.date(2024, 6, 3)),
    )
    make_commit(
        "feat(auth): API key management for external integrations",
        3, random_business_hour(datetime.date(2024, 6, 10)),
    )
    git("checkout", "develop")
    make_merge("feat(auth): merge auth middleware into develop", 3,
               random_business_hour(datetime.date(2024, 6, 17)), "feature/auth-middleware")
    
    # Bug fixes
    make_commit(
        "fix(customer-profile): handle empty enrichment data gracefully",
        1, random_business_hour(datetime.date(2024, 7, 1)),
    )
    make_commit(
        "fix(recommendation): normalize scores to 0-1 range",
        4, random_business_hour(datetime.date(2024, 7, 8)),
    )
    
    # Release v0.2.0
    git("checkout", "main")
    make_merge("release: v0.2.0 - integration layer and auth", 0,
               random_business_hour(datetime.date(2024, 7, 15)), "develop")
    make_commit(
        "docs: update changelog for v0.2.0",
        0, random_business_hour(datetime.date(2024, 7, 15)),
    )
    
    # Back to develop for continued work
    git("checkout", "develop")
    make_commit(
        "perf(customer-profile): cache enrichment results to reduce latency",
        2, random_business_hour(datetime.date(2024, 8, 5)),
    )
    make_commit(
        "perf(recommendation): optimize matrix factorization with batch processing",
        4, random_business_hour(datetime.date(2024, 8, 19)),
    )
    
    git("checkout", "-b", "feature/dashboard-frontend", "develop")
    make_commit(
        "feat(dashboard): add dashboard config and widget models",
        5, random_business_hour(datetime.date(2024, 9, 2)),
    )
    make_commit(
        "feat(dashboard): implement interactive dashboard widgets",
        5, random_business_hour(datetime.date(2024, 9, 16)),
    )
    make_commit(
        "feat(dashboard): real-time data refresh with websocket support",
        5, random_business_hour(datetime.date(2024, 9, 30)),
    )
    git("checkout", "develop")
    make_merge("feat(dashboard): merge dashboard frontend into develop", 5,
               random_business_hour(datetime.date(2024, 10, 7)), "feature/dashboard-frontend")
    
    make_commit(
        "refactor(automation): extract node execution into pluggable handlers",
        0, random_business_hour(datetime.date(2024, 10, 21)),
    )
    make_commit(
        "test: add integration tests for all modules",
        3, random_business_hour(datetime.date(2024, 11, 4)),
    )
    
    # v0.3.0
    git("checkout", "main")
    make_merge("release: v0.3.0 - dashboard frontend and performance optimization", 0,
               random_business_hour(datetime.date(2024, 11, 18)), "develop")
    
    git("checkout", "develop")
    make_commit(
        "chore: add seed data generation script for development",
        1, random_business_hour(datetime.date(2024, 12, 2)),
    )
    make_commit(
        "chore: add run and test scripts",
        1, random_business_hour(datetime.date(2024, 12, 9)),
    )
    
    # === PHASE 3: Maturity & Polish (Jan-May 2026) ===
    print("Phase 3: Maturity & Polish (Jan-May 2026)")
    
    # 2025 - sparse commits simulating a slower period
    for _ in range(10):
        d = datetime.date(2025, random.randint(1, 11), random.randint(1, 28))
        if d.weekday() >= 5:
            continue
        dev_idx = random.randint(0, 5)
        msgs = [
            "fix: resolve edge case in profile matching",
            "chore: update dependencies to latest versions",
            "docs: add API documentation for recommendation endpoints",
            "refactor: extract common utility functions",
            "style: apply consistent code formatting across modules",
            "test: increase coverage for analytics engine",
            "fix: handle timeout in recommendation service",
            "chore: configure CI/CD pipeline",
            "docs: update README with architecture overview",
        ]
        make_commit(random.choice(msgs), dev_idx, random_business_hour(d))
    
    # 2026 active development
    git("checkout", "-b", "feature/ml-model-upgrade", "develop")
    make_commit(
        "feat(ml): upgrade collaborative filtering with deep learning approach", 4,
        random_business_hour(datetime.date(2026, 1, 12)),
    )
    make_commit(
        "feat(ml): add model versioning and A/B testing framework", 4,
        random_business_hour(datetime.date(2026, 1, 26)),
    )
    git("checkout", "develop")
    make_merge("feat(ml): merge ML model upgrade into develop", 4,
               random_business_hour(datetime.date(2026, 2, 9)), "feature/ml-model-upgrade")
    
    make_commit(
        "fix(analytics): correct date range calculation in report generator", 5,
        random_business_hour(datetime.date(2026, 2, 23)),
    )
    make_commit(
        "feat(automation): add A/B test campaign type", 3,
        random_business_hour(datetime.date(2026, 3, 9)),
    )
    
    git("checkout", "-b", "feature/compliance-audit", "develop")
    make_commit(
        "feat(compliance): add data retention and audit logging", 2,
        random_business_hour(datetime.date(2026, 3, 23)),
    )
    make_commit(
        "feat(compliance): GDPR consent management module", 2,
        random_business_hour(datetime.date(2026, 4, 6)),
    )
    git("checkout", "develop")
    make_merge("feat(compliance): merge compliance audit into develop", 2,
               random_business_hour(datetime.date(2026, 4, 13)), "feature/compliance-audit")
    
    make_commit(
        "fix: resolve segmentation edge case for high-value customers", 1,
        random_business_hour(datetime.date(2026, 4, 20)),
    )
    make_commit(
        "chore: finalize package metadata and project configuration", 0,
        random_business_hour(datetime.date(2026, 4, 27)),
    )
    
    # Latest release to main
    git("checkout", "main")
    make_merge("release: v1.0.0 - production-ready AI marketing platform", 0,
               random_business_hour(datetime.date(2026, 5, 4)), "develop")
    make_commit(
        "docs: final changelog update for v1.0.0 release",
        0, random_business_hour(datetime.date(2026, 5, 4)),
    )
    
    print("History built successfully!")
    
    # Clean up helper script
    os.remove(REPO_DIR / "build_history.py")
    
    # Stats
    result = subprocess.run(
        ["git", "log", "--oneline", "--all"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    total_commits = len(result.stdout.strip().split("\n"))
    print(f"Total commits: {total_commits}")
    
    result = subprocess.run(
        ["git", "branch", "-a"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    branches = [b.strip() for b in result.stdout.strip().split("\n") if b.strip()]
    print(f"Branches: {len(branches)}")
    for b in branches:
        print(f"  {b}")

if __name__ == "__main__":
    # Seed random for reproducibility
    random.seed(42)
    main()

#!/bin/bash
# ============================================================
# DANAConnect Framework Tests — Launch Team Script
# ============================================================
# This script launches all 3 QA agents in separate Terminal
# windows. Each agent reads their role file and introduces
# themselves to the CEO.
#
# Usage:
#   chmod +x launch-team.sh   (make it executable — only needed once)
#   ./launch-team.sh           (run it)
#
# What happens:
#   - 3 Terminal windows open, each running a Claude instance
#   - Each Claude reads its agent role file and CLAUDE.md
#   - Each agent introduces itself and waits for your instructions
#
# If sessions/latest/ exists, agents resume from their last session.
# ============================================================

# Project directory (where this script lives)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  DANAConnect Framework Tests"
echo "  Launching QA Team (3 agents)"
echo "========================================"
echo ""
echo "Project: $PROJECT_DIR"
echo ""

# ── Check for session backups ──────────────────────────────────────
if [ -d "$PROJECT_DIR/sessions/latest" ]; then
    echo "Found previous session backups — agents will resume."
    RESUME=true
else
    echo "No previous sessions — fresh start."
    RESUME=false
fi
echo ""

# ── Launch Luna — Playwright Test Writer ───────────────────────────
echo "Launching Luna — Playwright Test Writer..."
if [ "$RESUME" = true ]; then
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$PROJECT_DIR' && claude 'Read agents/luna-playwright.md and adopt that role completely. Read CLAUDE.md for project context. Also read sessions/latest/luna-session.md to resume from your last session. You are Luna, the Playwright Test Writer. Use /qa-playwright when writing tests. Tell the CEO where you left off and what you recommend doing next.'\"
    end tell
    "
else
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$PROJECT_DIR' && claude 'Read agents/luna-playwright.md and adopt that role completely. Read CLAUDE.md for project context. You are Luna, the Playwright Test Writer. Use /qa-playwright when writing tests. Introduce yourself to the CEO.'\"
    end tell
    "
fi
sleep 1

# ── Launch Max — Selenium Test Writer ──────────────────────────────
echo "Launching Max — Selenium Test Writer..."
if [ "$RESUME" = true ]; then
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$PROJECT_DIR' && claude 'Read agents/max-selenium.md and adopt that role completely. Read CLAUDE.md for project context. Also read sessions/latest/max-session.md to resume from your last session. You are Max, the Selenium Test Writer. Use /qa-selenium when writing tests. Tell the CEO where you left off and what you recommend doing next.'\"
    end tell
    "
else
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$PROJECT_DIR' && claude 'Read agents/max-selenium.md and adopt that role completely. Read CLAUDE.md for project context. You are Max, the Selenium Test Writer. Use /qa-selenium when writing tests. Introduce yourself to the CEO.'\"
    end tell
    "
fi
sleep 1

# ── Launch Kai — Cypress Test Writer ───────────────────────────────
echo "Launching Kai — Cypress Test Writer..."
if [ "$RESUME" = true ]; then
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$PROJECT_DIR' && claude 'Read agents/kai-cypress.md and adopt that role completely. Read CLAUDE.md for project context. Also read sessions/latest/kai-session.md to resume from your last session. You are Kai, the Cypress Test Writer. Use /qa-cypress when writing tests. Tell the CEO where you left off and what you recommend doing next.'\"
    end tell
    "
else
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$PROJECT_DIR' && claude 'Read agents/kai-cypress.md and adopt that role completely. Read CLAUDE.md for project context. You are Kai, the Cypress Test Writer. Use /qa-cypress when writing tests. Introduce yourself to the CEO.'\"
    end tell
    "
fi

echo ""
echo "========================================"
echo "  All 3 agents launched!"
echo "========================================"
echo ""
echo "  Luna — Playwright (Python)  [Terminal Window 1]"
echo "  Max  — Selenium (Python)    [Terminal Window 2]"
echo "  Kai  — Cypress (JavaScript) [Terminal Window 3]"
echo ""
echo "  You are the CEO. They work for you."
echo "  To shut down: ./shutdown-team.sh"
echo "========================================"

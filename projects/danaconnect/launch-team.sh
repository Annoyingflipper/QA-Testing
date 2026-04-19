#!/bin/bash
# ============================================================
# LAUNCH-TEAM.SH — Opens 6 terminal windows, one per QA agent
# ============================================================
# Project: DANAConnect Platform QA
# Usage: ./launch-team.sh
#
# Opens 6 new Terminal windows, each running Claude Code with
# a specific QA team member's role. If a previous session backup
# exists (from shutdown-team.sh), agents read it and resume
# where they left off.
# ============================================================

PROJECT_DIR="/Users/vmaniglia/Documents/GitHub/QA-Testing/projects/danaconnect"
LATEST_SESSION="$PROJECT_DIR/sessions/latest"

echo "Launching DANAConnect QA Team..."
echo ""

# Check if there's a previous session to resume from
if [ -d "$LATEST_SESSION" ]; then
    echo "Previous session found — agents will resume where they left off."
    echo ""
    RESUME_INSTRUCTION="Then check if the file sessions/latest/SESSION_FILE exists. If it does, read it carefully — it contains your progress from the last session. Tell the CEO what you were working on and what you recommend doing next. If the file does not exist, start fresh."
else
    echo "No previous session found — starting fresh."
    echo ""
    RESUME_INSTRUCTION="This is a fresh session with no prior work."
fi

# ── Helper function to build the prompt for each agent ───────
# This keeps the osascript blocks cleaner and consistent.
build_prompt() {
    local ROLE_FILE=$1
    local NAME=$2
    local TITLE=$3
    local SESSION_FILE=$4
    local LOWER_NAME=$5
    local RESUME=$(echo "$RESUME_INSTRUCTION" | sed "s/SESSION_FILE/$SESSION_FILE/g")

    # Check if a dispatch task file exists for this agent
    local DISPATCH=""
    if [ -f "$PROJECT_DIR/dispatch/${LOWER_NAME}-task.md" ]; then
        DISPATCH="Then read dispatch/${LOWER_NAME}-task.md — this is your task assignment from Alex. Tell the CEO what you have been assigned and start working on it."
    fi

    echo "Read the file agents/$ROLE_FILE and adopt that role completely. Read CLAUDE.md for project context. You are $NAME, the $TITLE. $RESUME $DISPATCH Introduce yourself to the CEO."
}

# 1. Alex — QA Lead
PROMPT=$(build_prompt "alex-qa-lead.md" "Alex" "QA Lead" "alex-session.md" "alex")
osascript -e "
tell application \"Terminal\"
    do script \"cd $PROJECT_DIR && claude '$PROMPT'\"
    set custom title of front window to \"Alex — QA Lead\"
end tell
"
sleep 1

# 2. Jordan — Functional QA
PROMPT=$(build_prompt "jordan-functional-qa.md" "Jordan" "Functional QA Engineer" "jordan-session.md" "jordan")
osascript -e "
tell application \"Terminal\"
    do script \"cd $PROJECT_DIR && claude '$PROMPT'\"
    set custom title of front window to \"Jordan — Functional QA\"
end tell
"
sleep 1

# 3. Riley — UI/UX QA
PROMPT=$(build_prompt "riley-ui-qa.md" "Riley" "UI/UX QA Engineer" "riley-session.md" "riley")
osascript -e "
tell application \"Terminal\"
    do script \"cd $PROJECT_DIR && claude '$PROMPT'\"
    set custom title of front window to \"Riley — UI/UX QA\"
end tell
"
sleep 1

# 4. Sam — Security QA
PROMPT=$(build_prompt "sam-security-qa.md" "Sam" "Security QA Engineer" "sam-session.md" "sam")
osascript -e "
tell application \"Terminal\"
    do script \"cd $PROJECT_DIR && claude '$PROMPT'\"
    set custom title of front window to \"Sam — Security QA\"
end tell
"
sleep 1

# 5. Morgan — Performance QA
PROMPT=$(build_prompt "morgan-performance-qa.md" "Morgan" "Performance QA Engineer" "morgan-session.md" "morgan")
osascript -e "
tell application \"Terminal\"
    do script \"cd $PROJECT_DIR && claude '$PROMPT'\"
    set custom title of front window to \"Morgan — Performance QA\"
end tell
"
sleep 1

# 6. Casey — Automation Engineer
PROMPT=$(build_prompt "casey-automation.md" "Casey" "Test Automation Engineer" "casey-session.md" "casey")
osascript -e "
tell application \"Terminal\"
    do script \"cd $PROJECT_DIR && claude '$PROMPT'\"
    set custom title of front window to \"Casey — Automation\"
end tell
"

echo ""
echo "All 6 QA team members launched!"
echo ""
echo "Terminal windows:"
echo "  Alex    — QA Lead (strategy, coordination)"
echo "  Jordan  — Functional QA (business logic, workflows)"
echo "  Riley   — UI/UX QA (visual, accessibility)"
echo "  Sam     — Security QA (OWASP, auth, injection)"
echo "  Morgan  — Performance QA (load, speed, metrics)"
echo "  Casey   — Automation (Selenium, Playwright, Cypress, Jenkins)"
echo ""
echo "To shut down and save progress: ./shutdown-team.sh"
echo ""
echo "You are the CEO. Give each team member their marching orders!"

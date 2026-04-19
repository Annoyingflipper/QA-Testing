#!/bin/bash
# ============================================================
# DISPATCH-TEAM.SH — Tells all agents to check their assignments
# ============================================================
# Project: DANAConnect Platform QA
#
# WORKFLOW:
#   1. You brief Alex (QA Lead) in Alex's terminal window
#   2. Alex writes task files to dispatch/ for each agent
#   3. You run this script: ./dispatch-team.sh
#   4. Every agent reads their assignment and starts working
#   5. Agents write results to dispatch/results/
#
# HOW TO RUN:
#   From any terminal:     ./dispatch-team.sh
#   From an agent window:  ! ./dispatch-team.sh
#   From main session:     Tell Claude to "dispatch the team"
# ============================================================

PROJECT_DIR="/Users/vmaniglia/Documents/GitHub/QA-Testing/projects/danaconnect"

echo "Dispatching assignments to all agents..."
echo ""

# ── Define agents (must match window titles from launch-team.sh) ──
AGENTS=(
    "Alex|alex"
    "Jordan|jordan"
    "Riley|riley"
    "Sam|sam"
    "Morgan|morgan"
    "Casey|casey"
)

DISPATCHED=0

for agent_entry in "${AGENTS[@]}"; do
    IFS='|' read -r NAME LOWER_NAME <<< "$agent_entry"

    # Check if this agent has an assignment file
    ASSIGNMENT="$PROJECT_DIR/dispatch/${LOWER_NAME}-task.md"

    if [ -f "$ASSIGNMENT" ]; then
        # Send the agent a message to read their assignment
        FOUND=$(osascript << APPLESCRIPT 2>/dev/null
tell application "Terminal"
    set found to false
    set windowList to every window
    repeat with w in windowList
        try
            if name of w contains "$NAME" then
                do script "Read the file dispatch/${LOWER_NAME}-task.md — this is your assignment from Alex (QA Lead). Read it carefully, then tell the CEO what you're about to do and start working. When you finish a task, write your results to dispatch/results/${LOWER_NAME}-results.md. If you have findings for another team member, write a handoff file to docs/handoffs/." in w
                set found to true
            end if
        end try
    end repeat
    return found
end tell
APPLESCRIPT
)
        if [ "$FOUND" = "true" ]; then
            echo "  [dispatched] $NAME — reading dispatch/${LOWER_NAME}-task.md"
            DISPATCHED=$((DISPATCHED + 1))
        else
            echo "  [not found]  $NAME — window not found"
        fi
    else
        echo "  [no task]    $NAME — no assignment file (dispatch/${LOWER_NAME}-task.md)"
    fi

done

echo ""
if [ "$DISPATCHED" -gt 0 ]; then
    echo "$DISPATCHED agent(s) dispatched. They'll introduce their tasks to you."
    echo ""
    echo "Check each agent's terminal window — they're reading their assignments now."
    echo "Results will appear in dispatch/results/ as they work."
else
    echo "No agents dispatched. Make sure:"
    echo "  1. Alex has written task files in dispatch/"
    echo "  2. Agent terminal windows are open (run ./launch-team.sh first)"
fi

#!/bin/bash
# ============================================================
# SHUTDOWN-TEAM.SH — Gracefully shuts down all QA agents
# ============================================================
# Run from any terminal: ./shutdown-team.sh
# Run from an agent window: ! ./shutdown-team.sh
# ============================================================

PROJECT_DIR="/Users/vmaniglia/Documents/GitHub/QA-Testing/projects/danaconnect"
SESSIONS_DIR="$PROJECT_DIR/sessions"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="$SESSIONS_DIR/$TIMESTAMP"

echo "Initiating QA Team shutdown..."
echo "Session backups will be saved to: sessions/$TIMESTAMP/"
echo ""

mkdir -p "$BACKUP_DIR"

# Agent list: Name|Role|lowercase
AGENTS="Alex|QA Lead|alex
Jordan|Functional QA|jordan
Riley|UI/UX QA|riley
Sam|Security QA|sam
Morgan|Performance QA|morgan
Casey|Automation|casey"

FOUND_COUNT=0

echo "$AGENTS" | while IFS='|' read -r NAME ROLE LOWER_NAME; do
    BACKUP_FILE="$BACKUP_DIR/${LOWER_NAME}-session.md"

    # Pre-create backup file with header
    cat > "$BACKUP_FILE" <<HEADER
# Session Backup: $NAME — $ROLE
# Saved: $(date +"%Y-%m-%d %H:%M:%S")
# Project: DANAConnect Platform QA

> Agent did not write a backup. Check terminal for unsaved work.

---

HEADER

    # Build the message to send to the agent
    MSG="Write a session backup to the file $BACKUP_FILE. Include these sections exactly: ## Status - what you were actively working on, ## Completed - list everything you finished with specific file names and test case IDs, ## In Progress - partially done work and its current state, ## Next Steps - what you recommend doing next in priority order, ## Findings - any bugs or issues or observations or cross-team handoff items, ## Blockers - anything preventing progress. Be thorough and specific. After writing the file, say BACKUP COMPLETE."

    # Send to the agent's Terminal window via AppleScript
    osascript -e "
tell application \"Terminal\"
    set windowList to every window
    repeat with w in windowList
        try
            if name of w contains \"$NAME\" then
                do script \"$MSG\" in w
            end if
        end try
    end repeat
end tell
" 2>/dev/null

    echo "  [sent] $NAME - $ROLE"
done

echo ""
echo "Waiting 45 seconds for agents to write their backups..."

for i in 1 2 3 4 5 6 7 8 9; do
    sleep 5
    ELAPSED=$((i * 5))
    echo "  ... ${ELAPSED}s elapsed"
done

echo ""
echo "Sending exit commands to all agents..."

# First, send /exit to each Claude session to quit gracefully.
# This ends the claude process so Terminal won't ask to terminate.
echo "$AGENTS" | while IFS='|' read -r NAME ROLE LOWER_NAME; do
    osascript -e "
tell application \"Terminal\"
    set windowList to every window
    repeat with w in windowList
        try
            if name of w contains \"$NAME\" then
                do script \"/exit\" in w
            end if
        end try
    end repeat
end tell
" 2>/dev/null
    echo "  [exit sent] $NAME"
done

echo "Waiting 5 seconds for Claude sessions to close..."
sleep 5

# Now send 'exit' to close the shell itself
echo "$AGENTS" | while IFS='|' read -r NAME ROLE LOWER_NAME; do
    osascript -e "
tell application \"Terminal\"
    set windowList to every window
    repeat with w in windowList
        try
            if name of w contains \"$NAME\" then
                do script \"exit\" in w
            end if
        end try
    end repeat
end tell
" 2>/dev/null
done

sleep 2

# Finally close any remaining windows without the terminate prompt
echo "Closing terminal windows..."
echo "$AGENTS" | while IFS='|' read -r NAME ROLE LOWER_NAME; do
    osascript -e "
tell application \"Terminal\"
    set windowList to every window
    repeat with w in windowList
        try
            if name of w contains \"$NAME\" then
                close w saving no
            end if
        end try
    end repeat
end tell
" 2>/dev/null
    echo "  [closed] $NAME"
done

# Write session summary
SUMMARY_FILE="$BACKUP_DIR/session-summary.md"
cat > "$SUMMARY_FILE" <<EOF
# Session Summary — $(date +"%Y-%m-%d %H:%M:%S")

## Team Shutdown

All agents were asked to save progress and shut down.

## Backup Files

| Agent | Role | Backup File |
|-------|------|-------------|
| Alex | QA Lead | alex-session.md |
| Jordan | Functional QA | jordan-session.md |
| Riley | UI/UX QA | riley-session.md |
| Sam | Security QA | sam-session.md |
| Morgan | Performance QA | morgan-session.md |
| Casey | Automation | casey-session.md |

## To Resume

Run ./launch-team.sh to relaunch all agents.
Each agent will automatically read their latest backup and resume.
EOF

# Update latest symlink
ln -sfn "$BACKUP_DIR" "$SESSIONS_DIR/latest"

echo ""
echo "======================================="
echo "  Shutdown complete!"
echo "======================================="
echo ""
echo "Session backups: sessions/$TIMESTAMP/"
echo ""
echo "  alex-session.md"
echo "  jordan-session.md"
echo "  riley-session.md"
echo "  sam-session.md"
echo "  morgan-session.md"
echo "  casey-session.md"
echo "  session-summary.md"
echo ""
echo "To resume later: ./launch-team.sh"
echo "Agents will pick up where they left off."

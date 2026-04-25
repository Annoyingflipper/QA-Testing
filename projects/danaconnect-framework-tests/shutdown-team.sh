#!/bin/bash
# ============================================================
# DANAConnect Framework Tests — Shutdown Team Script
# ============================================================
# This script creates a session backup directory and reminds
# agents to save their progress before closing.
#
# Usage:
#   ./shutdown-team.sh
#   Or from inside an agent's Claude window: ! ./shutdown-team.sh
#
# What happens:
#   1. Creates sessions/<timestamp>/ directory
#   2. Creates placeholder files for each agent's session backup
#   3. Updates sessions/latest symlink
#   4. Reminds you to tell each agent to save their progress
#   5. Commits all work to git
# ============================================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SESSION_DIR="$PROJECT_DIR/sessions/$TIMESTAMP"

# Resolve the previous "latest" target (if any) BEFORE we move the symlink.
# Used below to carry the CEO live journal forward.
PREV_LATEST=""
if [ -L "$PROJECT_DIR/sessions/latest" ]; then
    PREV_LATEST="$(readlink "$PROJECT_DIR/sessions/latest")"
    # readlink may return relative or absolute — normalize
    case "$PREV_LATEST" in
        /*) ;;
        *) PREV_LATEST="$PROJECT_DIR/sessions/$PREV_LATEST" ;;
    esac
fi

echo "========================================"
echo "  DANAConnect Framework Tests"
echo "  Shutting Down QA Team"
echo "========================================"
echo ""

# ── Create session backup directory ────────────────────────────────
mkdir -p "$SESSION_DIR"
echo "Session directory: $SESSION_DIR"
echo ""

# ── Create placeholder backup files ───────────────────────────────
for agent in luna max kai; do
    cat > "$SESSION_DIR/${agent}-session.md" << EOF
# Session Backup: ${agent}
# Saved: $TIMESTAMP
# Project: DANAConnect Framework Tests

## Status
(Agent should fill this in before closing)

## Completed
- (List completed tasks)

## In Progress
- (List in-progress tasks)

## Next Steps
- (What to do next session)

## Findings
- (Bugs, observations, handoffs)

## Blockers
- (Anything preventing progress)
EOF
done

# ── CEO live journal: preserve continuity across shutdowns ───────
# If a previous CEO session file exists, copy it forward so the new
# `latest/ceo-session.md` continues the same live journal. The PREV_LATEST
# directory still holds the snapshot at this shutdown moment.
if [ -n "$PREV_LATEST" ] && [ -f "$PREV_LATEST/ceo-session.md" ]; then
    cp "$PREV_LATEST/ceo-session.md" "$SESSION_DIR/ceo-session.md"
    echo "Carried CEO live journal forward from previous session."
else
    cat > "$SESSION_DIR/ceo-session.md" << EOF
# CEO Session — DANAConnect Framework Tests
# Last updated: $TIMESTAMP

## Where we left off
(Fresh start — no prior CEO session.)

## Decisions log

## Completed work (chronological)

## In progress

## Next step (top priority)

## Open questions / awaiting CEO input

## Blockers

## Notes for next session
EOF
    echo "Created blank CEO session file (no prior journal found)."
fi

# ── Create session summary placeholder ────────────────────────────
cat > "$SESSION_DIR/session-summary.md" << EOF
# Session Summary
# Date: $TIMESTAMP
# Project: DANAConnect Framework Tests

## Team Snapshot
| Agent | Role | Status | Key Output |
|-------|------|--------|------------|
| Luna | Playwright Test Writer | | |
| Max | Selenium Test Writer | | |
| Kai | Cypress Test Writer | | |

## Overall Progress
- Test cases written:
- Tests automated:
- Bugs found:

## Recommended Next Steps
1.
2.
3.
EOF

# ── Update latest symlink ─────────────────────────────────────────
rm -f "$PROJECT_DIR/sessions/latest"
ln -s "$SESSION_DIR" "$PROJECT_DIR/sessions/latest"
echo "Updated sessions/latest -> $TIMESTAMP"
echo ""

# ── Remind CEO to save agent progress ─────────────────────────────
echo "IMPORTANT: Before closing agent windows, tell each agent:"
echo ""
echo '  "Save your progress to sessions/latest/<your-name>-session.md'
echo '   Fill in what you completed, what is in progress, and next steps."'
echo ""
echo "The CEO session journal (sessions/latest/ceo-session.md) was carried"
echo "forward automatically — it should already reflect today's state if you"
echo "live-journaled. Review it once before opening a new CEO session."
echo ""

# ── Commit all work ───────────────────────────────────────────────
echo "Committing all work..."
cd "$PROJECT_DIR"
git add -A
git commit -m "chore: session backup $TIMESTAMP" 2>/dev/null

echo ""
echo "========================================"
echo "  Shutdown complete!"
echo "  Session saved to: sessions/$TIMESTAMP/"
echo "  To resume: ./launch-team.sh"
echo "========================================"

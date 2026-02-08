# Agent/Assistant Instructions for CPTRed-2026

## Session Start / Resume
Before doing any task:
1. Read `CLAUDE.md` (this file).
2. Read `README.md`.
3. **Check for unmerged chatlogs**:
   - Look for assistant-specific chatlogs: `chatlogs/chat_claude_YYYY-MM-DD.md`, `chatlogs/chat_copilot_YYYY-MM-DD.md`, etc.
   - If multiple assistant-specific chatlogs exist for the same date without a merged version, note this for potential merge operation.
4. Read the latest chatlog(s) to reconstruct *last status*:
   - **Claude Code specific**: Look for `chatlogs/chat_claude_YYYY-MM-DD.md` (your dedicated chatlog)
   - If no Claude chatlog exists for today, create `chatlogs/chat_claude_YYYY-MM-DD.md` and add a "Session Start" entry.
   - Also check the unified `chatlogs/chat_YYYY-MM-DD.md` for context from other assistants.

Then:
5. Reconstruct the current project status **from files** (not memory): last completed step, current blockers, and next intended step.
6. Identify and open the **minimum relevant files** for the current request before editing or implementing.

## Logging Discipline (mandatory)
During an active session:
- Update the chatlog **after each interaction**.
- Chatlogs are **append-only**.
- Each update must include:
  - **Assistant attribution**: Mark each chatlog entry with which assistant made the changes (e.g., "Claude Code", "GitHub Copilot", "ChatGPT", etc.)
  - Files changed/created (exact names)
  - Commands run (exact commands)
  - Outputs generated (exact filenames/paths)
  - Decisions made + rationale
  - Open questions / blockers
  - Next steps
  - Context summary of what is going on in the session
  - Recent user messages (verbatim excerpts)
  - Run specs for important runs (script path, command, inputs, outputs, model, parameters, date, success counts)
  - For any replication script execution: record full run specs in the chatlog so the user can retain the info (script path, exact command, inputs, outputs, model, parameters, date, success counts).
  - Output hygiene: do not reuse output files across different runs or parameter settings; use a new output filename or folder to avoid mixing results, and ask if unsure.

## Chatlog Attribution Format
When making chatlog entries, use this format to clearly identify the assistant:

```markdown
## [Timestamp] - Claude Code

### User Request
[Brief summary of user's request]

### Actions Taken
- [Action 1]
- [Action 2]

### Files Modified
- [File path 1]
- [File path 2]

### Next Steps
- [Next step 1]
```

## Daily Chatlog Documentation

### Concurrent Operation (Multiple Assistants)
To avoid chatlog conflicts when multiple assistants work simultaneously:

**Claude Code specific chatlog**:
- Claude Code must use: `chatlogs/chat_claude_YYYY-MM-DD.md`
- Update this file **every assistant turn**
- This prevents conflicts with other assistants (GitHub Copilot, ChatGPT, etc.) who use their own files

**Other assistants**:
- GitHub Copilot: `chatlogs/chat_copilot_YYYY-MM-DD.md`
- ChatGPT: `chatlogs/chat_chatgpt_YYYY-MM-DD.md`
- etc.

### Session End Merge Procedure
**At the end of each session**, merge all assistant-specific chatlogs into the unified daily chatlog:
1. Check for assistant-specific chatlogs: `chat_claude_YYYY-MM-DD.md`, `chat_copilot_YYYY-MM-DD.md`, etc.
2. If multiple exist, merge them chronologically by timestamp into `chat_YYYY-MM-DD.md`
3. Preserve all assistant attribution headers (e.g., "Claude Code", "GitHub Copilot")
4. Keep assistant-specific files as archives or delete after successful merge
5. Document the merge in the unified chatlog

### Unmerged Chatlog Check
**At session start**, check for unmerged assistant-specific chatlogs from previous sessions:
- If found, offer to merge them before proceeding with new work
- This ensures complete session history in the unified daily chatlog

### Legacy Format
- Unified chatlog: `chatlogs/chat_YYYY-MM-DD.md` (used when only one assistant is active, or as merge target)

## README Updates (significant changes only)
Update `README.md` when any of the following occurs:
- Protocol/method changes
- New scripts/pipelines added
- File naming conventions change
- Reproduction steps change
- New results are generated that affect interpretation

Edits must be minimal and dated (prefer a "Changelog / Recent Updates" section).

Last Updated: January 26, 2026 (Concurrent workflow added)

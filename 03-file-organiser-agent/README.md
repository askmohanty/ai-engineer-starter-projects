# 03 · File organiser agent

An agent that tidies a folder by moving files into sensible subfolders. This is the first agent that **changes** something, so it's built defensively:

- **Dry run by default:** nothing moves unless you pass `--apply`.
- **Sandboxed:** every path is checked to be inside the folder you gave it.
- **No delete tool:** the agent can't do what it has no tool for.

**You learn:** giving an agent several tools; designing tools so a mistake by the model can't do damage.

```bash
mkdir -p /tmp/messy && touch /tmp/messy/{invoice.pdf,photo.jpg,setup.exe,notes.txt,data.xlsx}
python 03-file-organiser-agent/agent.py /tmp/messy            # see the plan
python 03-file-organiser-agent/agent.py /tmp/messy --apply    # do it
```

## Try this

1. Ask it (by editing the prompt) to move a file to `../outside`. What stops it?
2. Change the system prompt to sort by year (using `modified`) instead of type.
3. Add an `undo` feature: record every move in a list and add a tool that reverses the last one.
4. Should a "rename file" tool also be dry-run by default? Add one and decide.

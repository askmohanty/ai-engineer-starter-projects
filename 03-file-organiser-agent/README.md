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

## How it works (theory)

Once an agent can **change** things, the question is no longer "will it give a good answer?" but "what's the worst it could do?" Models misread instructions, and their input can be manipulated (**prompt injection**). So you design tools assuming the model will sometimes ask for the wrong thing:

- **Least privilege:** the agent has `list_files` and `move_file` only. There is no delete tool, so deletion is impossible, whatever the prompt says.
- **Sandboxing:** `inside_root()` resolves every path and refuses anything outside the root folder, including tricks like `../`.
- **Dry run by default:** the safe mode is the default; doing it for real needs an explicit human decision (`--apply`).
- **Fail loudly:** an existing destination raises an error instead of silently overwriting.

`make_tools()` builds the tools in a **closure** around `root` and `apply`, so the model can't change those settings. They aren't tool arguments.

Read more: [Agent safety](../concepts/08-agent-safety.md) · [Tool calling and agents: designing good tools](../concepts/03-tool-calling-and-agents.md#designing-good-tools)

## Try this

1. Ask it (by editing the prompt) to move a file to `../outside`. What stops it?
2. Change the system prompt to sort by year (using `modified`) instead of type.
3. Add an `undo` feature: record every move in a list and add a tool that reverses the last one.
4. Should a "rename file" tool also be dry-run by default? Add one and decide.

# Records docs/demo/attack.gif from a real run: `vhs docs/demo/attack.tape` from the repo root.
Output docs/demo/attack.gif
Set Shell "bash"
Set FontSize 15
Set Width 1300
Set Height 520
Set Padding 18
Set Theme "Catppuccin Mocha"
Set TypingSpeed 25ms

Hide
Type "export PS1='$ ' && uv sync -q && source .venv/bin/activate && clear" Enter
Sleep 4s
Show
Type "python -m red_teaming attack strict-guard" Enter
Sleep 3s
Type "python -m red_teaming attack medium-guard --hardened" Enter
Sleep 3s

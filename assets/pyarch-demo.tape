Output assets/pyarch-demo.gif

Set Shell "bash"
Set Width 1100
Set Height 650
Set FontSize 22
Set TypingSpeed 35ms
Set CursorBlink false
Set Theme { "name": "PyArch", "black": "#1e1e2e", "red": "#f38ba8", "green": "#a6e3a1", "yellow": "#f9e2af", "blue": "#89b4fa", "magenta": "#cba6f7", "cyan": "#94e2d5", "white": "#cdd6f4", "brightBlack": "#585b70", "brightRed": "#f38ba8", "brightGreen": "#a6e3a1", "brightYellow": "#f9e2af", "brightBlue": "#89b4fa", "brightMagenta": "#cba6f7", "brightCyan": "#94e2d5", "brightWhite": "#ffffff", "background": "#1e1e2e", "foreground": "#cdd6f4" }

Hide
Type "rm -rf pyarch_vhs_demo"
Enter
Type "clear"
Enter
Show

Type "pyarch init pyarch_vhs_demo --database sqlite"
Enter
Hide
Wait+Screen@5m /Project created:/
Show
Sleep 2s

Type "cd pyarch_vhs_demo"
Enter
Sleep 1s

Type "pyarch generate module users"
Enter
Wait+Screen@2m /Created module/
Sleep 2s

Type "pyarch info"
Enter
Wait+Screen@1m /PyArch project/
Sleep 4s

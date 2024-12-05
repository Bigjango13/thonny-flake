# thonny-flake
A [Thonny](https://github.com/thonny/thonny) plugin to add most of [flake8](https://github.com/PyCQA/flake8)'s warnings (except for [F401](https://www.flake8rules.com/rules/F401.html) because Thonny already warns when imported modules are unused).

## Installing
To install from pip3 using a terminal (or Powershell for Windows users):
```bash
pip3 install thonny-flake
# Or
python3 -m pip install thonny-flake
```

To install directly from Thonny:
1. Click "Tools" and then click "Manage Plug-ins..."
2. Search for "thonny-flake" in the input box.
3. Click install.

Either way, after installing you will need to restart Thonny for the changes to take effect.

## Debugging

### "The assistant menu is blank/not showing"

The warnings may not show if the file you are running is '\<untitled\>', save the file and try again. If not, look at the option below.

### "It doesn't show warnings!"

If it doesn't show any warnings on things that should be warnings, try these:

- Enable the assistant (Tools > Options > Assistant > enable all boxes you want, OK)
- Install flake8 (`python3 -m pip install flake8`)
- Restart Thonny
- Run your code again

If you still don't get warnings, then your code doesn't have any that flake8 detects.

# vivado-xpr-fixer
Fixes the project path name when using Vivado and Git together.

## Problem:

Vivado uses fully qualified pathnames when describing the location of the project file.
This causes issues when multiple people are working on multiple machines with the same Vivado project as the pathnames are likely to be different.

## Solution:

This script simply modifies the project file so that the pathname is fixed to the directory containing the project file.

## Usage:

Copy the `vivado-xpr-fixer.py` file to the root directory of the project.
You should commit this file to your repo.
This should also be the same directory that contains the Vivado XPR (project) file.

### Installing the Git Hook:

This script can operate as a git hook.
This means that it will automatically run whenever you perform a `git pull`.
You will need to install the git hook on every client machine as hooks aren't stored in the repository.

```python vivado-xpr-fixer.py install```

Note that "python" will need to be installed somewhere where git can execute it.

### Removing the Git Hook:

```python vivado-xpr-fixer.py install```

### Manually Updating the XPR File:

```python vivado-xpr-fixer.py update```

Note that you won't need to do this if you have it running via a git hook.

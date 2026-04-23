# Project Template Makefile

## Features
✔ Interactive
✔ Works in any folder
✔ Creates full project layout
✔ Git optional with: `make -f ~/.makefiles/project-templates.mk git DIR="X"`


### Step 1 - Create the folder 

`mkdir -p ~/.makefiles`

### Save the Makefile
`nano ~/.makefiles/project-templates.mk`

#### Makefile script
```makefile


```
Ctrl+x -> Y

### Export the Makefile

```bash
echo 'export MAKEFILES="$HOME/.makefiles/project-templates.mk"' >> ~/.bashrc
source ~/.bashrc
```

### Create the project creation script
#### Create bin folder
`mkdir -p ~/bin`

#### Create Script
`nano ~/bin/create-project.sh`

###### current-project.sh
Check scripts/

#### Make executable

`chmod +x ~/bin/create-project.sh`

### Add `~/bin` to PATH

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Create an alias for easier usage

```bash
echo 'alias make-newproject="~/bin/create-project.sh"' >> ~/.bashrc
source ~/.bashrc
```

### Use it

```bash
cd <PATH/TO/DESTINATION/FOLDER>
make-newproject
```



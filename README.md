# Vim extension for FHI-aims input files

Filetype detection and syntax highlighting for [FHI-aims](https://fhi-aims.org/) input files.
This is useful for quick check of invalid keywords.

**N.B.**: the list of keywords is not complete.

## Screenshots

control file
![control.in](figures/demo_control.png)

geometry file
![geometry.in](figures/demo_geometry.png)

## Prerequisites

- Python 3
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

## Usage

1. Clone this repository to vim configuration repository, e.g. "~/.vim/after"
2. Run

   ```shell
   python3 generate.py
   ```

3. By default it will create 3 files (also create directory when necessary)
   - `ftdetect/aimsin.vim`
   - `ftplugin/aimsin.vim`
   - `syntax/aimsin.vim`

   The file name `aimsin` can be changed by option `--filetype` of `generate.py`

## Example use

Assume the prerequisites are satisfied.

Vim
```shell
mkdir -p ~/.vim/after
cd ~/.vim/after
git clone https://github.com/minyez/vim-aims-input
cd vim-aims-input
python3 generate.py -d ..
```

NeoVim
```shell
mkdir -p ~/.config/nvim/after
cd ~/.config/nvim/after
git clone https://github.com/minyez/vim-aims-input
cd vim-aims-input
python3 generate.py -d ..
```

## Configuration and extension

To add more keywords, you can create an custom configuration file, for example `custom.yml`.
The basic syntax is
```yaml
[SyntaxName]:
  group: [VimHlg]
  prefix: "prefix\\s\\+"
  tags:
  - tag1
  - tag2
```
This will highlight the combined keywords `prefix tag1` and `prefix   tag2` using the Vim highlight
group `VimHlg`. `custom.yml` can be parsed via the `-c`/`--extra-configs` flag

```shell
python3 generate.py -c custom.yml
```

The syntax groups in `syntax.yml` can serve as examples.

Please note that if multiple `SyntaxName` of syntax groups are found, only the last one parsed will be used.
The following group names are reserved in the main config file `syntax.yml`:

- `General`
- `Output`
- `Species`

If you want to add keywords to these groups, please modify `syntax.yml`.

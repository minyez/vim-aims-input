#!/usr/bin/env python3
import argparse
import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def generate_ftdetect(d, filetype: str, force: bool = False):
    dirname = os.path.join(d, "ftdetect")
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fn = os.path.join(dirname, "{}.vim".format(filetype))
    if os.path.exists(fn) and not force:
        print("{} exists. Use -f to overwrite".format(fn))
        return

    with open(fn, 'w') as h:
        print("\" This file is generated automatically. Manual edit might be lost", file=h)
        print(r"""augroup filetype_{filetype}
  autocmd!
  autocmd BufNewFile,BufRead geometry*.in,geometry.in[_.]*,control*.in,control.in[_.]* set filetype={filetype}
  autocmd BufNewFile,BufRead *
      \ if (getline(1) =~? "^#%FHI-aims") || (getline(3) =~? "^#  FHI-aims code project") |
      \     set filetype={filetype} |
      \ endif
augroup END""".format(filetype=filetype), file=h)


def generate_ftplugin(d, filetype: str, force: bool = False):
    dirname = os.path.join(d, "ftplugin")
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fn = os.path.join(dirname, "{}.vim".format(filetype))
    if os.path.exists(fn) and not force:
        print("{} exists. Use -f to overwrite".format(fn))
        return

    with open(fn, 'w') as h:
        print("\" This file is generated automatically. Manual edit might be lost", file=h)
        print("""set syntax={filetype}
setlocal comments=:#
setlocal commentstring=#%s""".format(filetype=filetype), file=h)


def generate_syntax(tags_yaml, d, filetype: str, force: bool = False):
    dirname = os.path.join(d, "syntax")
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fn = os.path.join(dirname, "{}.vim".format(filetype))
    if os.path.exists(fn) and not force:
        print("{} exists. Use -f to overwrite".format(fn))
        return

    highlight_groups = {}
    try:
        with open(tags_yaml, 'r') as h:
            highlight_groups = load(h, Loader=Loader)
    except KeyError:
        pass

    with open(fn, 'w') as h:
        def p(*args):
            print(*args, file=h)

        p("\" This file is generated automatically. Manual edit might be lost")
        p("syn match aimsComment\t\"#.*$\"")
        p("hi def link aimsComment\tComment")
        p()
        for name, config in highlight_groups.items():
            group = config["group"]
            tags = config["tags"]

            match_strs = []
            if len(tags) > 0:
                match_str = "\\v<({})>".format("|".join(tags))
                if "prefix" in config:
                    match_str = config["prefix"] + match_str
                match_strs.append(match_str)
            if "extras" in config:
                match_strs.extend(config["extras"])
            for s in match_strs:
                p("syn match aims{}\t\"^\\s*{}\"".format(name, s))
            if len(match_strs) > 0:
                p("hi def link aims{}\t{}".format(name, group))
                p()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--syntax-yaml", type=str, default="syntax.yml",
                   help="YAML file to configure Vim syntax")
    p.add_argument("--ft", "--filetype", dest="filetype", type=str, default="aimsin",
                   help="Filetype for aims inputs in Vim, default: aimsin")
    p.add_argument("-d", dest="directory", type=str, default=".",
                   help="Vim configuration directory, default: pwd")
    p.add_argument("-f", dest="force", action="store_true", default="aimsin",
                   help="Force overwrite")
    args = p.parse_args()

    if not os.path.exists(args.syntax_yaml):
        raise FileNotFoundError("{} is not found".format(args.syntax_yaml))

    generate_ftdetect(args.directory, args.filetype, args.force)
    generate_ftplugin(args.directory, args.filetype, args.force)
    generate_syntax(args.syntax_yaml, args.directory, args.filetype, args.force)

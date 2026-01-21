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
        print("{} exists. Skip".format(fn))
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
        print("{} exists. Skip".format(fn))
        return

    with open(fn, 'w') as h:
        print("\" This file is generated automatically. Manual edit might be lost", file=h)
        print("""set syntax={filetype}
setlocal comments=:#
setlocal commentstring=#%s""".format(filetype=filetype), file=h)


def generate_syntax(d, filetype: str, force: bool = False, *syntax_yamls):
    dirname = os.path.join(d, "syntax")
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fn = os.path.join(dirname, "{}.vim".format(filetype))
    if os.path.exists(fn) and not force:
        print("{} exists. Skip".format(fn))
        return

    highlight_groups = {}
    for y in syntax_yamls:
        try:
            with open(y, 'r') as h:
                highlight_groups.update(load(h, Loader=Loader))
        except FileNotFoundError:
            print(f"{y} not found, skip")

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
    p.add_argument("-c", "--extra-configs", type=str,
                   default=[], nargs="+",
                   help="Additional YAML files to configure Vim syntax")
    p.add_argument("--ft", "--filetype", dest="filetype", type=str, default="aimsin",
                   help="Filetype for aims inputs in Vim, default: aimsin")
    p.add_argument("-d", dest="directory", type=str, default=".",
                   help="Vim configuration directory, default: pwd")
    p.add_argument("-f", dest="force", action="store_true",
                   help="Force overwrite")
    args = p.parse_args()

    generate_ftdetect(args.directory, args.filetype, args.force)
    generate_ftplugin(args.directory, args.filetype, args.force)
    generate_syntax(args.directory, args.filetype, args.force, "syntax.yml", *(args.extra_configs))

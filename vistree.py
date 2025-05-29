"""
Print a tree of the current directory, excluding files and directories
that match rules in .gitignore, .git, and ./venv/.

This script is intended to be run from the command line, and will write
two files: vistree.txt and structure.dot. The first is a plain text
representation of the tree, and the second is a DOT file that can be
used to generate a visual representation of the tree using Graphviz.

Example output (vistree.txt):

foo/
bar/
baz
quux

Example output (structure.dot):

digraph G {
  rankdir=TB;
  node [shape=box, fontname="Arial"];
  "foo" [label="foo"];
  "foo" -> "bar";
  "bar" [label="bar"];
  "foo" -> "baz";
  "baz" [label="baz"];
  "foo" -> "quux";
  "quux" [label="quux"];
}

"""

import os
from pathlib import Path
import fnmatch

def is_gitignored(path, gitignore_rules):
    """
    Return True if the path matches any of the gitignore rules
    or is in .git or ./venv directories.

    :param path: The path to check
    :param gitignore_rules: A list of gitignore rules
    :return: True if the path is ignored, False otherwise
    """
    # Convert path to relative and normalize for comparison
    relpath = str(Path(path).relative_to(Path.cwd()))
    # Check if any gitignore rule matches
    excluded_dirs = ['.git', 'venv']
    if any(relpath.startswith(d) for d in excluded_dirs):
        return True
    for rule in gitignore_rules:
        if fnmatch.fnmatch(relpath, rule) or fnmatch.fnmatch(os.path.basename(path), rule):
            return True
    return False

def parse_gitignore(gitignore_path):
    """
    Parse the .gitignore file and return a list of rules.

    :param gitignore_path: The path to the .gitignore file
    :return: A list of gitignore rules
    """
    rules = []
    if not gitignore_path.exists():
        return rules
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Convert to glob pattern (simplified)
                if line.endswith('/'):
                    line = line[:-1] + '/**'
                else:
                    line = line
                rules.append(line)
    return rules

def traverse_and_print(path, prefix, gitignore_rules, tree, dot_nodes, parent_node=None):
    """
    Recursively traverse the directory tree and generate a plain text
    representation and a DOT file.

    :param path: The current path
    :param prefix: The indentation prefix
    :param gitignore_rules: A list of gitignore rules
    :param tree: A list of lines for the plain text representation
    :param dot_nodes: A list of lines for the DOT file
    :param parent_node: The parent node ID in the DOT file
    """
    path = Path(path)
    if is_gitignored(str(path), gitignore_rules):
        return
    if path.is_dir():
        name = path.name
        if parent_node is None:
            node_id = name
        else:
            node_id = f'{parent_node}_{name}'
        dot_nodes.append(f'"{node_id}" [label="{name}"];')
        if parent_node is not None:
            dot_nodes.append(f'"{parent_node}" -> "{node_id}";')
        tree.append(f'{prefix}{name}/')
        items = sorted(os.listdir(path))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            new_prefix = prefix + ('    ' if is_last else '│   ')
            traverse_and_print(
                path / item,
                new_prefix,
                gitignore_rules,
                tree,
                dot_nodes,
                node_id
            )
    else:
        name = path.name
        node_id = f'{parent_node}_{name}'
        dot_nodes.append(f'"{node_id}" [label="{name}"];')
        if parent_node is not None:
            dot_nodes.append(f'"{parent_node}" -> "{node_id}";')
        tree.append(f'{prefix}{name}')

def main():
    """
    Main entry point.

    This function is called when the script is run from the command line.
    """
    cwd = Path.cwd()
    gitignore_path = cwd / '.gitignore'
    gitignore_rules = parse_gitignore(gitignore_path)
    tree = []
    dot_nodes = []

    traverse_and_print(cwd, '', gitignore_rules, tree, dot_nodes)

    # Write ASCII tree
    with open('vistree.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(tree))

    # Write DOT file
    with open('structure.dot', 'w') as f:
        f.write('digraph G {\n')
        f.write('  rankdir=TB;\n')
        f.write('  node [shape=box, fontname="Arial"];\n')
        f.write('\n'.join(dot_nodes) + '\n')
        f.write('}\n')

if __name__ == '__main__':
    main()


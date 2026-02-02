"""
Directory Tree Visualization Tool

Generates visual representations of the project directory structure,
excluding files and directories that match .gitignore rules.

Outputs:
    - vistree.txt: Plain text ASCII tree representation
    - structure.dot: Graphviz DOT file for visual diagrams

Usage:
    python vistree.py

The script automatically:
- Reads .gitignore rules from the project root
- Excludes .git/ and venv/ directories
- Traverses the directory tree recursively
- Generates both text and DOT format outputs

Example vistree.txt output:
    foo/
    │   bar/
    │   │   baz
    │   quux

Example structure.dot output:
    digraph G {
      rankdir=TB;
      node [shape=box, fontname="Arial"];
      "foo" [label="foo"];
      "foo" -> "bar";
      ...
    }

To generate a visual diagram from structure.dot:
    dot -Tpng structure.dot -o structure.png

Author: HebiKata Contributors
License: Apache 2.0
"""

import os
from pathlib import Path
import fnmatch


def is_gitignored(path, gitignore_rules):
    """
    Check if a path should be excluded based on gitignore rules.
    
    Checks both specific gitignore patterns and hardcoded exclusions
    (.git, venv directories).
    
    Args:
        path (str): The path to check (can be file or directory)
        gitignore_rules (List[str]): List of gitignore pattern strings
        
    Returns:
        bool: True if the path should be ignored, False otherwise
        
    Note:
        Uses fnmatch for pattern matching, which supports wildcards like
        *, ?, and [seq]
    """
    # Convert path to relative and normalize for comparison
    relpath = str(Path(path).relative_to(Path.cwd()))
    
    # Check if any gitignore rule matches
    excluded_dirs = ['.git', 'venv']
    if any(relpath.startswith(d) for d in excluded_dirs):
        return True
    
    # Check against gitignore patterns
    for rule in gitignore_rules:
        if fnmatch.fnmatch(relpath, rule) or fnmatch.fnmatch(os.path.basename(path), rule):
            return True
    return False


def parse_gitignore(gitignore_path):
    """
    Parse .gitignore file and extract pattern rules.
    
    Reads the .gitignore file line by line and converts patterns into
    a format suitable for fnmatch comparison. Ignores comments and
    empty lines.
    
    Args:
        gitignore_path (Path): Path to the .gitignore file
        
    Returns:
        List[str]: List of gitignore pattern strings
        
    Note:
        This is a simplified implementation. Full gitignore spec includes
        negation (!), directory-only patterns (/), and more complex rules.
    """
    rules = []
    if not gitignore_path.exists():
        return rules
    
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Convert directory patterns to glob patterns
                if line.endswith('/'):
                    line = line[:-1] + '/**'
                else:
                    line = line
                rules.append(line)
    return rules


def traverse_and_print(path, prefix, gitignore_rules, tree, dot_nodes, parent_node=None):
    """
    Recursively traverse directory tree and generate output.
    
    Walks the directory structure, respecting gitignore rules, and builds
    both plain text and DOT graph representations simultaneously.
    
    Args:
        path (Path): Current path being processed
        prefix (str): Indentation prefix for text output (e.g., "│   ")
        gitignore_rules (List[str]): Gitignore patterns to exclude
        tree (List[str]): Accumulator for text output lines
        dot_nodes (List[str]): Accumulator for DOT graph statements
        parent_node (str, optional): Parent node ID in DOT graph
        
    Side Effects:
        Modifies tree and dot_nodes lists in place
        
    Note:
        Uses depth-first traversal with alphabetical sorting at each level
    """
    path = Path(path)
    
    # Skip if path matches gitignore rules
    if is_gitignored(str(path), gitignore_rules):
        return
    
    if path.is_dir():
        name = path.name
        # Generate unique node ID for DOT graph
        if parent_node is None:
            node_id = name
        else:
            node_id = f'{parent_node}_{name}'
        
        # Add DOT graph nodes and edges
        dot_nodes.append(f'"{node_id}" [label="{name}"];')
        if parent_node is not None:
            dot_nodes.append(f'"{parent_node}" -> "{node_id}";')
        
        # Add to text tree
        tree.append(f'{prefix}{name}/')
        
        # Recursively process directory contents
        items = sorted(os.listdir(path))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            # Adjust prefix for tree structure visualization
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
        # Handle files
        name = path.name
        node_id = f'{parent_node}_{name}'
        
        # Add to DOT graph
        dot_nodes.append(f'"{node_id}" [label="{name}"];')
        if parent_node is not None:
            dot_nodes.append(f'"{parent_node}" -> "{node_id}";')
        
        # Add to text tree
        tree.append(f'{prefix}{name}')


def main():
    """
    Main entry point for directory tree visualization.
    
    Orchestrates the entire process:
    1. Load gitignore rules from .gitignore
    2. Traverse directory tree from current working directory
    3. Generate plain text ASCII tree
    4. Generate Graphviz DOT file
    5. Write both outputs to files
    
    Outputs:
        vistree.txt: Plain text tree visualization
        structure.dot: Graphviz DOT file for diagram generation
    """
    cwd = Path.cwd()
    gitignore_path = cwd / '.gitignore'
    gitignore_rules = parse_gitignore(gitignore_path)
    
    # Accumulators for output
    tree = []
    dot_nodes = []
    
    # Traverse and build both representations
    traverse_and_print(cwd, '', gitignore_rules, tree, dot_nodes)
    
    # Write ASCII tree to file
    with open('vistree.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(tree))
    
    # Write DOT file for Graphviz
    with open('structure.dot', 'w') as f:
        f.write('digraph G {\n')
        f.write('  rankdir=TB;\n')
        f.write('  node [shape=box, fontname="Arial"];\n')
        f.write('\n'.join(dot_nodes) + '\n')
        f.write('}\n')
    
    print("✅ Generated vistree.txt and structure.dot")
    print("   To create a visual diagram: dot -Tpng structure.dot -o structure.png")


# Entry point when script is run directly
if __name__ == '__main__':
    main()


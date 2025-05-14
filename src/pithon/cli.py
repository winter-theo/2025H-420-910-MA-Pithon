from pathlib import Path
import sys
import os
from pithon.evaluator.evaluator import empty_env, evaluate
from pithon.parser.simpleparser import SimpleParser
from pithon.syntax import PiAssignment

def run_cli():
    parser = SimpleParser()
    env = empty_env()
    
    print("🐍 Pithon CLI!")

    while True:
        try:
            line = input("> ").strip()
            if line.lower() in ("exit", "quit"):
                print("Au revoir 👋.")
                break
            if not line:
                continue
            tree = parser.parse(line)
            result = evaluate(tree, env)
            if not isinstance(tree, PiAssignment):
                print(result)
        except Exception as e:
            print(f"Erreur: {e}")

def run_file(filename):
    parser = SimpleParser()
    env = empty_env()
    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()
    tree = parser.parse(source)
    evaluate(tree, env)

def run_tests():
    test_dir = Path("test")
    files = [f for f in os.listdir(test_dir) if f.startswith("test-") and f.endswith(".py")]
    if not files:
        print("Aucun fichier de test trouvé.")
        return
    for fname in sorted(files):
        path = os.path.join(test_dir, fname)
        print(f"--- Test : {fname} ---")
        try:
            run_file(path)
        except Exception as e:
            print(f"Erreur dans {fname}: {e}")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            run_tests()
        else:
            run_file(sys.argv[1])
    else:
        run_cli()
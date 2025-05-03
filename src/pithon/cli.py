from pithon.parser.simpleparser import SimpleParser
from pithon.evaluator.evaluator import empty_env, evaluate

def main():
    parser = SimpleParser()
    
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
            print(tree)
        except Exception as e:
            print(f"Erreur: {e}")
from pithon.evaluator.evaluator import empty_env, evaluate
from pithon.parser.simpleparser import SimpleParser
from pithon.syntax import PiAssignment


def main():
    parser = SimpleParser()
    env = empty_env()
    
    print("Hello, Pithon CLI!")

    while True:
        try:
            line = input("> ").strip()
            if line.lower() in ("exit", "quit"):
                print("Exiting Pithon CLI.")
                break
            if not line:
                continue
            tree = parser.parse(line)
            result = evaluate(tree, env)
            if not isinstance(tree, PiAssignment):
                print(result)
        except Exception as e:
            print(f"Error: {e}")
from pithon.parser.simpleparser import SimpleParser


def main():
    parser = SimpleParser()
    
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
            print(tree)
        except Exception as e:
            print(f"Error: {e}")
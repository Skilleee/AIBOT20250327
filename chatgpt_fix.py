import os
import openai
import argparse
import ast
import re
import subprocess
import importlib.util
from datetime import datetime
from dotenv import load_dotenv

# Ladda .env-variabler
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

EXCLUDE_DIRS = {"venv", "__pycache__", ".git", "tests"}

# 🔁 Automatisk fallback-import

def dynamic_import(function_name, search_dirs=("utils", "notifications")):
    for folder in search_dirs:
        for root, _, files in os.walk(folder):
            for file in files:
                if not file.endswith(".py") or file.startswith("__"):
                    continue
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                        if f"def {function_name}(" in content:
                            module_name = os.path.splitext(os.path.relpath(path).replace(os.sep, "."))[0]
                            spec = importlib.util.spec_from_file_location(module_name, path)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            print(f"✅ Hittade '{function_name}' i {path}")
                            return getattr(module, function_name)
                except Exception:
                    continue
    print(f"❌ Kunde inte hitta funktionen '{function_name}' i projektet.")
    exit(1)

backup_file = dynamic_import("backup_file")
send_telegram_message = dynamic_import("send_telegram_message")

def is_python_file(filename):
    return filename.endswith(".py")

def find_all_python_files(include_tests=False):
    py_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if not file.endswith(".py"):
                continue
            if file.endswith(".bak"):
                continue
            if not include_tests:
                if file.startswith("test_") or file.endswith("_test.py"):
                    continue
                if file == "__init__.py":
                    continue
                if os.path.abspath(os.path.join(root, file)) == os.path.abspath(__file__):
                    continue
            py_files.append(os.path.join(root, file))
    return py_files

def parse_imports(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
            return {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        except Exception:
            return set()

def group_files_by_dependency(files, target_file=None):
    groups = []
    visited = set()
    for file in files:
        if file in visited:
            continue
        group = {file}
        imports = parse_imports(file)
        for other in files:
            if other == file:
                continue
            if any(os.path.basename(other).startswith(i) for i in imports):
                group.add(other)
        visited |= group
        groups.append(list(group))
    if target_file:
        for g in groups:
            if target_file in g:
                return [g]
        return [[target_file]]
    return groups

def run_python_file(filepath: str) -> str:
    try:
        result = subprocess.run(["python", filepath], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return result.stderr.strip()
    except Exception as e:
        return f"Kunde inte köra filen: {e}"
    return ""

def run_pytest() -> str:
    try:
        result = subprocess.run(["pytest", "--tb=short", "--maxfail=3"], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return result.stdout.strip() + "\n" + result.stderr.strip()
    except Exception as e:
        return f"Kunde inte köra pytest: {e}"
    return ""

def verify_post_refactor(files: list) -> str:
    output = ""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for file in files:
        error = run_python_file(file)
        if error:
            output += f"\n❌ Fel vid körning av `{file}` efter refaktorering:\n{error}\n"

    pytest_result = run_pytest()
    if pytest_result:
        output += "\n❌ Pytest-fel efter refaktorering:\n" + pytest_result

    if not output:
        output = "✅ Alla filer kördes korrekt och pytest passerade utan fel."

    os.makedirs("logs", exist_ok=True)
    with open("logs/post_check.log", "a", encoding="utf-8") as f:
        f.write(f"\n--- {now} ---\n")
        f.write("Refaktorerade filer:\n" + "\n".join(files) + "\n")
        f.write(output + "\n")

    return output.strip()

def refactor_code(code: str, file_path: str = "", error: str = "", context_files: dict = None) -> str:
    prompt = f'''
Du är en mycket skicklig Python-utvecklare och expert på att felsöka och refaktorisera kod med hjälp av AI.

Filen `{file_path}` innehåller följande kod:
```python
{code}
```
'''

    if context_files:
        prompt += "\nHär är relaterade beroendefiler i samma projekt:\n"
        for ctx_path, ctx_code in context_files.items():
            prompt += f"\nFil: `{ctx_path}`:\n```python\n{ctx_code}\n```\n"

    if error:
        prompt += f'''
När koden kördes uppstod följande fel:
```
{error}
```

Analysera och åtgärda detta fel i filen `{file_path}`. Förbättra samtidigt kodkvaliteten utan att ändra funktionalitet.
'''
    else:
        prompt += f'''
Refaktorisera filen `{file_path}` så att den blir mer robust, läsbar och idiomatisk enligt PEP8.
'''

    prompt += "\n[OBS] Returnera endast den fullständiga refaktorerade koden för filen. Ingen extra text.\n"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du är en expert på Python och refaktorering."},
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        error_msg = f"[GPT FEL] {file_path}: {e}\n"
        print(error_msg)
        os.makedirs("logs", exist_ok=True)
        with open("logs/gpt_errors.log", "a", encoding="utf-8") as logf:
            logf.write(error_msg)
        send_telegram_message(f"⚠️ GPT FEL i `{file_path}`:\n{e}", TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
        return ""

def handle_group(files, dry_run=False, notify=True):
    full_code = ""
    file_errors = {}

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            full_code += f"\n# Fil: {file}\n" + f.read()

        error_output = run_python_file(file)
        if error_output:
            file_errors[file] = error_output

    pytest_errors = run_pytest()
    if pytest_errors:
        file_errors["pytest"] = pytest_errors

    target_file = files[0]
    error_text = file_errors.get(target_file, "")
    if "pytest" in file_errors:
        error_text += "\n\n[Pytest-fel]:\n" + file_errors["pytest"]

    refactored = refactor_code(full_code, file_path=target_file, error=error_text)
    if not refactored:
        print(f"Ingen refaktorering genomförd för {target_file} p.g.a. GPT-fel.")
        return

    split_code = re.split(r"# Fil: (.+)", refactored)[1:]
    changed_files = []

    for i in range(0, len(split_code), 2):
        file_name = split_code[i].strip()
        new_code = split_code[i + 1].strip()
        if not os.path.exists(file_name):
            continue
        if not dry_run:
            backup_file(file_name)
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(new_code)
        changed_files.append(file_name)

    postcheck = verify_post_refactor(changed_files)

    if notify:
        send_telegram_message("✅ Refaktorerade filer:\n" + "\n".join(changed_files) + "\n\n" + postcheck, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    else:
        print("Refaktorerade filer:\n" + "\n".join(changed_files))
        print(postcheck)

def main():
    parser = argparse.ArgumentParser(description="GPT-Refactor CLI")
    parser.add_argument("--file", type=str, help="Refaktorisera en specifik fil")
    parser.add_argument("--group", type=str, help="Refaktorisera filens beroendegrupp")
    parser.add_argument("--all", action="store_true", help="Refaktorisera hela projektet")
    parser.add_argument("--dry-run", action="store_true", help="Visa men skriv inte över filer")
    parser.add_argument("--no-telegram", action="store_true", help="Hoppa över Telegram-meddelande")
    parser.add_argument("--include-tests", action="store_true", help="Inkludera testfiler i refaktorisering")

    args = parser.parse_args()
    all_files = find_all_python_files(include_tests=args.include_tests)

    if args.file:
        handle_group([args.file], dry_run=args.dry_run, notify=not args.no_telegram)
    elif args.group:
        groups = group_files_by_dependency(all_files, args.group)
        for g in groups:
            handle_group(g, dry_run=args.dry_run, notify=not args.no_telegram)
    elif args.all:
        groups = group_files_by_dependency(all_files)
        for g in groups:
            handle_group(g, dry_run=args.dry_run, notify=not args.no_telegram)
    else:
        print("Använd --file, --group eller --all för att specificera vad som ska refaktoreras.")

if __name__ == "__main__":
    main()

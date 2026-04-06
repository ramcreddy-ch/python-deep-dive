# 29. Advanced Regex & Strings — Pattern Matching & Text Processing

> "Some people, when confronted with a problem, think 'I know, I'll use regular expressions.' Now they have two problems. However, an expert knows that Regex is the most powerful weapon in the developer's arsenal for 'Data Extraction', 'Log Parsing', and 'Input Validation'."

---

## ❓ The 'Why' (High-Level)
In the real world, data is messy. It's often "Unstructured Text"—like a log file, an email body, or a website's HTML. If you try to find an email address using just `if...else` statements, you will write 1,000 lines of code. **Regular Expressions (Regex)** allow you to write a single-line "Pattern" that describes the data you want. A principal engineer uses Regex to "Extract" signals from a "Noise" of millions of characters in milliseconds.

---

## 🌱 Module 1: The Basics (Junior) — The Search
Regex is about "Describing" a string rather than "Naming" it.

### 1. The Survival Kit: Searching
```python
import re
text = "The user's email is ram@work.com"
# Searching for an email pattern
match = re.search(r"\w+@\w+\.com", text)
if match: print(f"Found: {match.group()}")
```

### 2. Basic Wildcards
- **`.`**: Any character.
- **`*`**: Zero or more times.
- **`+`**: One or more times.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Character Classes
Mid-level engineers use "Shortcuts" to describe data types.

### 1. Common Shortcuts
- **`\d`**: Any Digit (0-9).
- **`\w`**: Any Word character (a-z, 0-9, _).
- **`\s`**: Any Whitespace (space, tab, newline).

### 2. Groups `()`
Groups allow you to extract specific **parts** of a match.
- **Example**: Searching for "ID: 123" and only extracting the "123".

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Lookarounds
Senior engineers use "Checkpoints" to match text ONLY if it is followed or preceded by something else.

### 1. Lookahead `(?=...)`
Find "Python" only if it is followed by "Masterclass."
```python
re.findall(r"Python(?= Masterclass)", "Python Masterclass vs Python Basics")
# Returns: ['Python'] (only the first one!)
```

### 2. Named Groups `(?P<name>...)`
Instead of using group numbers like `group(1)`, give them **Names** so your code is more readable.
- **Regex**: `(?P<year>\d{4})-(?P<month>\d{2})`
- **Code**: `match.group("year")`

---

## 🔥 Module 4: Principal Architect (Principal) — The "Nuclear Ops"
At the highest level, you manage the "Complexity" and "Safety" of the regex engine.

### 1. Catastrophic Backtracking
Some "bad" regex patterns (e.g., `(a+)+$`) can take **trillions of years** to run on a long string of "aaaaaab". This will crash your server (ReDoS attack).
- **Expert fix**: Be specific. Never use "nested" quantifiers on wildcards.

### 2. Verbose Regex (`re.VERBOSE`)
Regex is notoriously hard to read. A principal engineer uses `VERBOSE` to add **Comments** and **Newlines** to their patterns.
```python
pattern = re.compile(r"""
    (?P<user>\w+)  # Match the username
    @              # Match the @ symbol
    (?P<domain>\w+) # Match the domain
""", re.VERBOSE)
```

---

## 🏗️ Case Study: The 50-Format Log Parser
A cybersecurity company needed to parse logs from 50 different firewalls (Cisco, Juniper, etc.), all with different time formats.
- **The Junior Approach**: Write 50 different `if...else` functions. (Incredibly slow and buggy).
- **The Principal Approach**: Built a single, **Multi-line Verbose Regex**. It used "Optional Groups" `(...)?` to account for the different fields.
- **Result**: Reduced the parser code from 4,000 lines to **40 lines**, making it 10x faster to maintain.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Regex for HTML
**NEVER** use Regex to parse HTML or XML (e.g., `<a href="(.*)">`). HTML is too complex for regex and will eventually break. **Expert fix**: Use a parser like **BeautifulSoup**.

### 2. Greedy Matching `.*`
By default, `.*` matches as much as possible. If you try to find text between `"quotes"`, it might match everything from the first quote to the **last** quote in the whole file. **Expert fix**: Use **Non-Greedy** matching `.*?`.

---

## 🎯 Top 20 Principal Interview Questions (Advanced Regex)

1. **Q: What is the difference between `re.match()` and `re.search()`?**
   - **Answer**: `re.match()` only checks for a match at the **Beginning** of the string. `re.search()` checks for a match **Anywhere** in the string.
2. **Q: What does the `r` prefix (raw string) do in regex?**
   - **Answer**: It tells Python to ignore "Backslashes" (`\`). Without it, `\n` is interpreted as a newline. With it, `\n` is passed directly to the regex engine as two characters.
3. **Q: Explain 'Greedy' vs 'Non-Greedy' matching.**
   - **Answer**: **Greedy** (`*`) tries to match the longest possible string. **Non-Greedy** (`*?`) tries to match the shortest possible string.
4. **Q: What is a 'Capture Group'?**
   - **Answer**: A part of a regex enclosed in parentheses `()`. It allows you to extract or refer back to a specific portion of the entire match.
5. **Q: How do you perform a 'Global' search (finding all matches)?**
   - **Answer**: Using `re.findall()` (returns a list of strings) or `re.finditer()` (returns an iterator of match objects, which is better for large data).
6. **Q: What are 'Anchors' (`^` and `$`)?**
   - **Answer**: `^` marks the **Start** of a string. `$` marks the **End** of a string. They ensure the pattern matches the entire line, not just a portion of it.
7. **Q: What is the purpose of `re.compile()`?**
   - **Answer**: It "pre-calculates" the regex pattern into a reusable object. If you are using the same regex 1,000,000 times, compiling it saves significant time.
8. **Q: Explain 'Lookahead' and 'Lookbehind'.**
   - **Answer**: They are "Checkpoints" that match text only if it's followed by (`Lookahead`) or preceded by (`Lookbehind`) another pattern, but won't include that other pattern in the final match.
9. **Q: What is 'Catastrophic Backtracking'?**
   - **Answer**: A performance nightmare where a poorly written regex takes an exponential amount of time to fail on a non-matching string, effectively freezing the CPU.
10. **Q: What is a 'Backreference'?**
    - **Answer**: Referring back to a previously captured group within the same regex (e.g., `(\w+)\s+\1` matches repeated words like "the the").
11. **Q: How do you handle 'Multiple Lines' with one regex?**
    - **Answer**: By using the `re.MULTILINE` flag. This makes `^` and `$` match the start and end of **Every Line**, rather than just the start and end of the entire string.
12. **Q: What does the `re.DOTALL` flag do?**
    - **Answer**: By default, the `.` (dot) matches everything EXCEPT a newline. `DOTALL` makes the dot match newline characters as well.
13. **Q: What is the purpose of `re.VERBOSE`?**
    - **Answer**: It ignores whitespace and allows for **Comments** inside the regex string, making the pattern much easier to read and maintain for humans.
14. **Q: How do you substitute text using Regex?**
    - **Answer**: Using `re.sub(pattern, replacement, string)`.
15. **Q: What is a 'Character Class'?**
    - **Answer**: A set of characters enclosed in square brackets `[abc]`. It matches any **one** of those characters. You can also use ranges like `[a-z0-9]`.
16. **Q: What is the difference between `\s` and `\S`?**
    - **Answer**: Lowercase `\s` matches any **Whitespace**. Uppercase `\S` matches anything that is **NOT** whitespace. (All caps usually means "NOT").
17. **Q: How do you match a literal `.` (dot)?**
    - **Answer**: Since the dot is a special wildcard, you must **Escape** it with a backslash: `\.`.
18. **Q: What is 'Atomic Grouping'?**
    - **Answer**: A way to disable "Backtracking" for a specific group, preventing performance issues on "bad" input strings.
19. **Q: Can Regex be used for 'Email Validation' reliably?**
    - **Answer**: Technically yes, but the official email spec is so complex that the resulting regex would be thousands of characters long. In production, use a library or just check for an `@` and a `.`.
20. **Q: How can you find the indices (start/end) of a match?**
    - **Answer**: By using the `.start()` and `.end()` methods of the match object returned by `re.search()`.

---

[Previous: Databases](28-database-engineering.md) | [Next: C-Extensions & Cython →](30-c-extensions-cython.md)

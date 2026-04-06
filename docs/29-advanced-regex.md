# 29. Advanced Regex — Complex Text Extraction & Backtracking

> "Regex is the 'Secret Language' of text processing. A junior uses it to find a word; an expert uses Lookaheads and Non-Capturing Groups to build high-performance log extractors and security filters that process millions of lines per second."

---

## 🌱 The Basics: Character Classes
The entry-level way to find patterns in text.

- `\d`: Digit (0-9).
- `\w`: Word (A-Z, 0-9, _).
- `\s`: Whitespace (tab, space).

```python
import re

# 1. Find all numbers in a string
nums = re.findall(r"\d+", "Error at line 102 and 105")
# Output: ["102", "105"]
```

---

## 🌿 Intermediate: Named Groups
`Named Groups` allow you to extract specific parts of a match into a dictionary-like object.

**Real Use (SRE/Log Analysis)**:
Extracting the IP and Status from a standard server log.

```python
import re

log = '192.168.1.101 - - [06/Apr] "GET /index" 200 512'
# 1. Using (?P<name>...)
pattern = r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).* (?P<status>\d{3}) (?P<size>\d+)"

match = re.search(pattern, log)
if match:
    print(f"IP: {match.group('ip')} | Status: {match.group('status')}")
```

---

## 🌳 Advanced: Lookaheads & Lookbehinds
Senior engineers use **Assertions** to match a word only if it is followed (or preceded) by another specific word, without including that second word in the match.

- **Lookahead `(?=...)`**: Check if the next characters match a pattern.

```python
# Match 'Ramchandra' only if followed by 'Chintala'
# Output: ["Ramchandra"] (the surname is NOT part of the match)
match = re.findall(r"Ramchandra(?= Chintala)", "Ramchandra Chintala")
```

---

## 🔥 Expert: Backtracking & ReDoS Security
Principal engineers understand that Regex is a **State Machine**. 

### 1. The Greedy Trap
`.*` is "Greedy" (it matches as much as possible). Use `.*?` (Lazy) to match only what is needed.

### 2. ReDoS (Regular Expression Denial of Service)
A malicious user can send a 100-character string that takes 5 minutes to process, crashing your application. This happens with "Nested Quantifiers" like `(a+)+$`.

```python
# Principal Pattern: Safe Regex. 
# 1. Avoid nested quantifiers.
# 2. Use 'Atomic Groups' where possible.
# 3. Always set a timeout if processing untrusted user input.
```

---

## 🎯 Top 20 Principal Interview Questions (Advanced Regex)

1. **Q: What is the difference between `re.search()` and `re.match()`?**
   - **Answer**: `re.match()` checks for a pattern only at the **Beginning** of the string. `re.search()` scans the **Entire** string for the first match it finds.
2. **Q: Explain 'Greedy' vs 'Lazy' (Non-Greedy) matching.**
   - **Answer**: **Greedy** (`*`, `+`) tries to match as much text as possible. **Lazy** (`*?`, `+?`) tries to match as **Little** as possible to satisfy the pattern.
3. **Q: What is a 'Non-Capturing Group' `(?:...)` and why use it?**
   - **Answer**: It groups logic (like an OR `(A|B)`) but tells the Regex engine **not to store the match in memory**. This is a high-performance optimization for scanning millions of logs.
4. **Q: What are 'Named Groups' `(?P<name>...)`?**
   - **Answer**: They allow you to assign a **Label** to a part of the matching pattern, making it much easier to extract data into a dictionary-like object (`match.group('name')`).
5. **Q: What is 'ReDoS' (Regular Expression Denial of Service)?**
   - **Answer**: A security vulnerability where a complex regex takes an extreme amount of CPU time to process a specific input, potentially crashing the entire application.
6. **Q: Explain 'Lookahead' and 'Lookbehind' assertions.**
   - **Answer**: They allow you to match a pattern only if it is **followed by** (`(?=...)`) or **preceded by** (`(?<=...)`) another pattern, but without including that second pattern in the actual match result.
7. **Q: What is 'Backtracking' in a Regex engine?**
   - **Answer**: The process where the engine "Gives Up" on a partial match and goes back to try a different path. Excessive backtracking is what causes ReDoS.
8. **Q: How do you handle 'Multiple Lines' in a long log file?**
   - **Answer**: Using the `re.MULTILINE` (or `re.M`) flag. This allows `^` and `$` to match the beginning and end of **each line** instead of just the whole string.
9. **Q: What is the `re.compile()` function and why use it?**
   - **Answer**: It "Pre-compiles" a regex pattern into a reusable object. If you are using the same pattern 1,000,000 times in a loop, pre-compiling is much faster because it only parses the pattern once.
10. **Q: What is the difference between `re.findall()` and `re.finditer()`?**
    - **Answer**: `findall()` returns a **List** of all matches (consuming memory). `finditer()` returns an **Iterator** (saving memory), which is preferred for massive text files.
11. **Q: How do you escape special characters (like `.` or `*`) in a pattern?**
    - **Answer**: Use a backslash (`\.`, `\*`) or use `re.escape(string)` to systematically escape all special characters in a piece of raw text.
12. **Q: What is 'Atomic Grouping' (available in some libraries, not CPython)?**
    - **Answer**: A pattern that tells the engine "Once you match this, don't ever backtrack into it." It's a key security measure against ReDoS.
13. **Q: What does the `.` (dot) character NOT match by default?**
    - **Answer**: It does not match the **Newline** character (`\n`). Use the `re.DOTALL` flag to make it match everything.
14. **Q: Explain the `\b` (Word Boundary) character.**
    - **Answer**: It matches the position between a word character (`\w`) and a non-word character. Use it to find a whole word (like "cat") without matching it inside another word (like "catalog").
15. **Q: What is 'Backreferencing' in a pattern?**
    - **Answer**: The ability to refer to a previous match in the same pattern (e.g., `(abc)\1` matches "abcabc").
16. **Q: How do you replace all occurrences of a pattern in a string?**
    - **Answer**: `re.sub(pattern, replacement, string)`.
17. **Q: What is a 'Verbal' Regex?**
    - **Answer**: Using the `re.VERBOSE` flag to allow **Comments** and whitespace inside your pattern, making complex regex much easier for a team to read and maintain.
18. **Q: How do you handle case-insensitive matching?**
    - **Answer**: Use the `re.IGNORECASE` (or `re.I`) flag.
19. **Q: What is the difference between `\d` and `[0-9]`?**
    - **Answer**: In Python 3, `\d` matches **Any Unicode Digit** (including Arabic or Hindi numbers), whereas `[0-9]` matches **only** ASCII numbers. Use `re.ASCII` if you want `\d` to only match 0-9.
20. **Q: Why should you avoid "Nested Quantifiers" (like `(a+)+$`)?**
    - **Answer**: They are the most common cause of **Exponential Backtracking**, which leads directly to ReDoS vulnerabilities.

---

[← Previous: Database Engineering](28-database-engineering.md) | [Next: C-Extensions →](30-python-c-api-extensions.md)

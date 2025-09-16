# fill_bat_positions_bert_charspan.py
# Usage: python fill_bat_positions_bert_charspan.py
# Overwrites /content/bat.csv (no header). 
# Writes:
#  - column 0: original sentence (unchanged)
#  - column 1: token index (0-based, includes special tokens)
#  - column 2: character span "start:end" (0-based, start inclusive, end exclusive)
#
# Notes:
#  - If multiple occurrences of "bat" exist in a sentence this will record the FIRST occurrence (left-to-right).
#  - Token index points to the first WordPiece token of the matched span.

import re
import sys
import pandas as pd
from transformers import AutoTokenizer

CSV_PATH = "/content/bat.csv"
MODEL_NAME = "bert-base-uncased"

def normalize_text_for_compare(s: str) -> str:
    """Normalize substring for comparison: strip surrounding non-word chars and lowercase."""
    if s is None:
        return ""
    s = str(s)
    s = s.strip()
    # remove leading/trailing punctuation/whitespace (keeps letters/digits/_)
    s = re.sub(r'^[^\w]+|[^\w]+$', '', s, flags=re.UNICODE)
    return s.lower()

def find_bat_token_and_char_span(sentence: str, tokenizer):
    """
    Return (token_index, char_start, char_end)
    - token_index: 0-based index in tokenized input including special tokens (or -1 if not found)
    - char_start, char_end: 0-based Python slice indices into the original sentence (or -1, -1 if not found)
    Strategy:
      1) Use offsets (fast tokenizer) to find a contiguous token span whose substring maps to 'bat' after normalization.
      2) Fallback: compare individual wordpiece token texts (strip '##') to 'bat'.
    """
    if sentence is None:
        return -1, -1, -1
    sent = str(sentence)
    enc = tokenizer(sent, return_offsets_mapping=True, add_special_tokens=True)
    tokens = tokenizer.convert_ids_to_tokens(enc["input_ids"])
    offsets = enc["offset_mapping"]
    n = len(tokens)
    target = "bat"

    # Primary: find contiguous span whose substring equals 'bat' after normalization
    for i in range(n):
        start_i, end_i = offsets[i]
        # skip special tokens with (0,0) offsets
        if start_i == end_i == 0:
            continue
        for j in range(i, n):
            s_j, e_j = offsets[j]
            if s_j == e_j == 0:
                break
            start_char = start_i
            end_char = e_j
            if end_char <= start_char:
                continue
            substring = sent[start_char:end_char]
            if normalize_text_for_compare(substring) == target:
                return i, start_char, end_char

    # Fallback: check single token pieces (strip '##')
    for i, tok in enumerate(tokens):
        s_i, e_i = offsets[i]
        if s_i == e_i == 0:
            continue
        tok_norm = tok.replace("##", "")
        tok_norm = normalize_text_for_compare(tok_norm)
        if tok_norm == target:
            return i, s_i, e_i

    # Not found
    return -1, -1, -1

def main(path: str):
    try:
        # Read CSV without header (first line is first sentence)
        df = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    except Exception as e:
        print(f"Error reading CSV '{path}': {e}", file=sys.stderr)
        sys.exit(1)

    if df.shape[1] == 0:
        print("CSV appears empty.", file=sys.stderr)
        sys.exit(1)

    # Ensure at least three columns exist (0: sentence, 1: token index, 2: char span)
    if df.shape[1] < 2:
        df[1] = ""
    if df.shape[1] < 3:
        df[2] = ""

    # Load fast tokenizer for offsets
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

    token_indices = []
    char_spans = []
    missing_rows = []

    for row_i, sent in enumerate(df[0].astype(str), start=1):  # row_i is 1-based for user messages
        token_idx, start_ch, end_ch = find_bat_token_and_char_span(sent, tokenizer)
        token_indices.append(int(token_idx) if token_idx != -1 else -1)
        if token_idx == -1:
            char_spans.append("")   # leave empty if not found
            missing_rows.append(row_i)
        else:
            char_spans.append(f"{start_ch}:{end_ch}")

    # Write results into columns 1 and 2
    df[1] = token_indices
    df[2] = char_spans

    try:
        # Overwrite CSV without header (preserve headerless format)
        df.to_csv(path, index=False, header=False)
    except Exception as e:
        print(f"Error writing CSV '{path}': {e}", file=sys.stderr)
        sys.exit(1)

    total = len(token_indices)
    found = sum(1 for x in token_indices if x != -1)
    print(f"Done. Wrote {total} rows to '{path}'. Found 'bat' in {found} rows; {total-found} not found.")
    if missing_rows:
        print("Rows where 'bat' was not located (1-based CSV row numbers):")
        print(", ".join(map(str, missing_rows)))
    print()
    print("Conventions used:")
    print(" - token index: 0-based and includes special tokens ([CLS] is index 0). Use this to index BERT outputs, e.g.")
    print("     outputs.last_hidden_state[batch_idx, token_index, :]")
    print(" - character span: 'start:end' with 0-based start inclusive, end exclusive (Python slicing).")
    print(" - If multiple 'bat' occurrences exist in a sentence, the FIRST (left-to-right) occurrence is recorded.")

if __name__ == '__main__':
    main(CSV_PATH)

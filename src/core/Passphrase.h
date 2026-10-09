/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
// Passphrase.h
// Draw words from a list and join them. The draw is supplied by the caller.
// Production calls PWSrand::RangeRand at the call site. This file does not.
//-----------------------------------------------------------------------------
#ifndef __PASSPHRASE_H
#define __PASSPHRASE_H

#include <cstddef>

#include "StringX.h"

// draw(n) returns a uniform value in [0, n). n is never zero.
typedef unsigned int (*PassphraseDraw)(size_t n);

// Default word count for the bundled EFF long list, and the default of the
// PassphraseWordCount preference.
const size_t kDefaultPassphraseWords = 6;

// Limits of the PassphraseWordCount preference.
constexpr int kMinPassphraseWords = 1;
constexpr int kMaxPassphraseWords = 99;

// count limited to [kMinPassphraseWords, kMaxPassphraseWords].
int ClampPassphraseWords(int count);

// A typed word count: a base-10 whole number with an optional sign and
// surrounding whitespace, clamped by ClampPassphraseWords. A number too large
// for an int clamps by its sign. Returns current when text is empty or is not
// a whole number.
int PassphraseWordCountFromText(const stringT &text, int current);

// Lowercase words, joined by a single hyphen, drawn with replacement.
// Returns empty, and does not call draw, when the list is empty, words is
// null, wordCount is zero, or draw is null. An out-of-range draw or a null
// word also returns empty, so nothing partial is kept.
StringX MakePassphrase(const char * const *words, size_t nWords,
                       size_t wordCount, PassphraseDraw draw);

// wordCount * log2(nWords). Zero when either argument is zero.
double PassphraseEntropyBits(size_t wordCount, size_t nWords);

// "6 x log2(7776) = 77.5 bits". Empty when wordCount or nWords is zero.
// This line does not say whether the result is strong.
StringX PassphraseEntropyLine(size_t wordCount, size_t nWords);

// True when Generate should make a passphrase rather than a password: only
// when this computer's passphrase policy is switched on and the entry uses
// the safe's default policy. An entry's own policy or a named policy wins.
bool GenerateMakesPassphrase(bool useLocalPolicy, bool entryOnSafeDefault);

// Bundled EFF long list: 7776 lowercase words. See docs/EFF/EFF-LONG-WORDLIST-NOTICE.txt.
const char * const *EffLongWords();
size_t EffLongWordCount();

#endif /* __PASSPHRASE_H */

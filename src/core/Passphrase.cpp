/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
#include <cmath>

#include "Passphrase.h"

static void AppendUnsigned(StringX &out, size_t n)
{
  wchar_t tmp[32];
  int i = 0;
  if (n == 0) {
    out.push_back(L'0');
    return;
  }
  while (n > 0 && i < 32) {
    tmp[i++] = static_cast<wchar_t>(L'0' + (n % 10));
    n /= 10;
  }
  while (i > 0)
    out.push_back(tmp[--i]);
}

static void AppendLowerAscii(StringX &out, const char *word)
{
  for (const unsigned char *p = reinterpret_cast<const unsigned char *>(word); *p != 0; ++p) {
    unsigned char c = *p;
    if (c >= 'A' && c <= 'Z')
      c = static_cast<unsigned char>(c - 'A' + 'a');
    out.push_back(static_cast<wchar_t>(c));
  }
}

StringX MakePassphrase(const char * const *words, size_t nWords,
                       size_t wordCount, PassphraseDraw draw)
{
  if (words == nullptr || nWords == 0 || wordCount == 0 || draw == nullptr)
    return StringX();

  StringX phrase;
  for (size_t i = 0; i < wordCount; ++i) {
    const unsigned int index = draw(nWords);
    if (index >= nWords)
      return StringX();
    const char *word = words[index];
    if (word == nullptr || word[0] == '\0')
      return StringX();
    if (i > 0)
      phrase.push_back(L'-');
    AppendLowerAscii(phrase, word);
  }
  return phrase;
}

double PassphraseEntropyBits(size_t wordCount, size_t nWords)
{
  if (wordCount == 0 || nWords == 0)
    return 0.0;
  return static_cast<double>(wordCount) * (std::log(static_cast<double>(nWords)) / std::log(2.0));
}

StringX PassphraseEntropyLine(size_t wordCount, size_t nWords)
{
  if (wordCount == 0 || nWords == 0)
    return StringX();

  const double bits = PassphraseEntropyBits(wordCount, nWords);
  // One decimal place. 6 * log2(7776) is 77.549, which is 77.5.
  const unsigned long tenths = static_cast<unsigned long>(std::lround(bits * 10.0));

  StringX line;
  AppendUnsigned(line, wordCount);
  line += L" x log2(";
  AppendUnsigned(line, nWords);
  line += L") = ";
  AppendUnsigned(line, tenths / 10);
  line.push_back(L'.');
  AppendUnsigned(line, tenths % 10);
  line += L" bits";
  return line;
}

bool GenerateMakesPassphrase(bool useLocalPolicy, bool entryOnSafeDefault)
{
  return useLocalPolicy && entryOnSafeDefault;
}

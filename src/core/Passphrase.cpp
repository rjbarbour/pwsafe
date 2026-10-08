/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
#include <charconv>
#include <cmath>
#include <limits>
#include <string>
#include <system_error>

#include "Passphrase.h"

static void AppendUnsigned(StringX &out, size_t n)
{
  wchar_t tmp[std::numeric_limits<size_t>::digits10 + 1];
  int i = 0;
  if (n == 0) {
    out.push_back(L'0');
    return;
  }
  while (n > 0) {
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

int ClampPassphraseWords(int count)
{
  if (count < kMinPassphraseWords)
    return kMinPassphraseWords;
  if (count > kMaxPassphraseWords)
    return kMaxPassphraseWords;
  return count;
}

int PassphraseWordCountFromText(const stringT &text, int current)
{
  const wchar_t *space = L" \t\r\n\v\f";
  const stringT::size_type first = text.find_first_not_of(space);
  if (first == stringT::npos)
    return current;
  const stringT::size_type last = text.find_last_not_of(space);

  stringT::size_type i = first;
  const bool negative = text[i] == L'-';
  if (negative || text[i] == L'+')
    ++i;
  if (i > last)
    return current;

  std::string number(negative ? "-" : "");
  for (; i <= last; ++i) {
    if (text[i] < L'0' || text[i] > L'9')
      return current;
    number.push_back(static_cast<char>(text[i]));
  }

  int count = 0;
  const std::from_chars_result r =
    std::from_chars(number.data(), number.data() + number.size(), count);
  if (r.ec == std::errc::result_out_of_range)
    return negative ? kMinPassphraseWords : kMaxPassphraseWords;
  return ClampPassphraseWords(count);
}

bool GenerateMakesPassphrase(bool useLocalPolicy, bool entryOnSafeDefault)
{
  return useLocalPolicy && entryOnSafeDefault;
}

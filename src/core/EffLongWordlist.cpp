/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
// Bundled EFF long wordlist. Words only; dice prefixes are not included.
// The readable copy is eff-long-wordlist.txt. EffLongWordlist.inc is that
// file as a string table and must stay in step with it.
#include "Passphrase.h"

#include "EffLongWordlist.inc"

static_assert(sizeof(kEffLongWords) / sizeof(kEffLongWords[0]) == kEffLongWordCount,
              "EFF long list must have 7776 words");
static_assert(kEffLongWordCount == 7776, "EFF long list is 7776 words");

const char * const *EffLongWords()
{
  return kEffLongWords;
}

size_t EffLongWordCount()
{
  return kEffLongWordCount;
}

const char *EffLongWordlistNotice()
{
  return
    "EFF long wordlist (7776 words). "
    "Copyright Electronic Frontier Foundation. "
    "Licensed under Creative Commons Attribution 3.0 (CC BY 3.0): "
    "https://creativecommons.org/licenses/by/3.0/ "
    "Source: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt";
}

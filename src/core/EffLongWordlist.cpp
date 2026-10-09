/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
// Bundled EFF long wordlist. Words only; dice prefixes are not included.
// EffLongWordlist.inc is the only copy of the list. Its header gives the
// source URL and the SHA-256 of EFF's original file.
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

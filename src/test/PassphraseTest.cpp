/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
// PassphraseTest.cpp: Unit tests for Diceware passphrase generation

#ifdef WIN32
#include "../ui/Windows/stdafx.h"
#endif
#include "core/Passphrase.h"
#include "gtest/gtest.h"
#include <string>

static unsigned int g_seq[8];
static size_t g_n, g_i;
static unsigned int FixedDraw(size_t n)
{
  EXPECT_EQ(n, g_n);
  return g_seq[g_i++];
}

TEST(PassphraseTest, known_draw)
{
  const char *words[] = {"Alpha", "beta", "GAMMA"};
  g_seq[0] = 2; g_seq[1] = 0; g_seq[2] = 1;
  g_n = 3; g_i = 0;
  StringX phrase = MakePassphrase(words, 3, 3, FixedDraw);
  EXPECT_EQ(std::wstring(L"gamma-alpha-beta"), std::wstring(phrase.c_str()));
  EXPECT_EQ(g_i, 3u);
  g_seq[0] = 0; g_seq[1] = 0;
  g_n = 3; g_i = 0;
  phrase = MakePassphrase(words, 3, 2, FixedDraw);
  EXPECT_EQ(std::wstring(L"alpha-alpha"), std::wstring(phrase.c_str()));
}

TEST(PassphraseTest, entropy_line)
{
  EXPECT_EQ(std::wstring(L"6 x log2(7776) = 77.5 bits"),
            std::wstring(PassphraseEntropyLine(6, 7776).c_str()));
  EXPECT_EQ(std::wstring(L"6 x log2(2048) = 66.0 bits"),
            std::wstring(PassphraseEntropyLine(6, 2048).c_str()));
  EXPECT_EQ(std::wstring(L"4 x log2(7776) = 51.7 bits"),
            std::wstring(PassphraseEntropyLine(4, 7776).c_str()));
  EXPECT_EQ(EffLongWordCount(), 7776u);
  EXPECT_STREQ(EffLongWords()[0], "abacus");
  EXPECT_STREQ(EffLongWords()[7775], "zoom");
}

TEST(PassphraseTest, fail_closed)
{
  const char *words[] = {"one"};
  g_n = 1; g_i = 0;
  EXPECT_TRUE(MakePassphrase(words, 0, 3, FixedDraw).empty());
  EXPECT_TRUE(MakePassphrase(nullptr, 1, 3, FixedDraw).empty());
  EXPECT_TRUE(MakePassphrase(words, 1, 0, FixedDraw).empty());
  EXPECT_TRUE(MakePassphrase(words, 1, 1, nullptr).empty());
  EXPECT_EQ(g_i, 0u); // invalid input never draws
  EXPECT_TRUE(PassphraseEntropyLine(0, 7776).empty());
  EXPECT_TRUE(PassphraseEntropyLine(4, 0).empty());
  EXPECT_DOUBLE_EQ(PassphraseEntropyBits(0, 7776), 0.0);
  g_seq[0] = 5; g_n = 1; g_i = 0;
  EXPECT_TRUE(MakePassphrase(words, 1, 1, FixedDraw).empty());
}

TEST(PassphraseTest, empty_word_fails_closed)
{
  const char *words[] = {"one", "", nullptr};
  g_n = 3;
  g_seq[0] = 0; g_seq[1] = 1; g_i = 0;
  EXPECT_TRUE(MakePassphrase(words, 3, 2, FixedDraw).empty());
  EXPECT_EQ(g_i, 2u);
  g_seq[0] = 2; g_i = 0;
  EXPECT_TRUE(MakePassphrase(words, 3, 1, FixedDraw).empty());
  EXPECT_EQ(g_i, 1u);
}

TEST(PassphraseTest, generate_decision)
{
  EXPECT_TRUE(GenerateMakesPassphrase(true, true));
  EXPECT_FALSE(GenerateMakesPassphrase(true, false));  // entry or named policy wins
  EXPECT_FALSE(GenerateMakesPassphrase(false, true));  // switch off: existing generator
  EXPECT_FALSE(GenerateMakesPassphrase(false, false));
}

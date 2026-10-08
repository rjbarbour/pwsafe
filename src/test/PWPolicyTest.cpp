/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
// PWPolicyTest.cpp: Characterisation tests for PWPolicy password generation
// and policy string parsing, as they behave before any passphrase change.

#ifdef WIN32
#include "../ui/Windows/stdafx.h"
#endif
#include "core/PWPolicy.h"
#include "core/PWCharPool.h"
#include "core/PWSprefs.h"
#include "gtest/gtest.h"

namespace {
const int kRuns = 50; // each generation test repeats to cover the random draw

int CountIn(const StringX &s, const stringT &set)
{
  int n = 0;
  for (auto c : s)
    if (set.find(c) != stringT::npos)
      n++;
  return n;
}

const stringT kLower(_T("abcdefghijklmnopqrstuvwxyz"));
const stringT kUpper(_T("ABCDEFGHIJKLMNOPQRSTUVWXYZ"));
const stringT kDigits(_T("0123456789"));
} // namespace

TEST(PWPolicyTest, all_classes_with_minimums)
{
  PWPolicy pol;
  pol.flags = PWPolicy::UseLowercase | PWPolicy::UseUppercase |
              PWPolicy::UseDigits | PWPolicy::UseSymbols;
  pol.length = 20;
  pol.lowerminlength = 3;
  pol.upperminlength = 4;
  pol.digitminlength = 2;
  pol.symbolminlength = 5;
  const stringT symbols = CPasswordCharPool::GetDefaultSymbols();

  for (int i = 0; i < kRuns; i++) {
    const StringX pw = pol.MakeRandomPassword();
    ASSERT_EQ(20u, pw.length());
    EXPECT_GE(CountIn(pw, kLower), 3);
    EXPECT_GE(CountIn(pw, kUpper), 4);
    EXPECT_GE(CountIn(pw, kDigits), 2);
    EXPECT_GE(CountIn(pw, symbols), 5);
    EXPECT_EQ(20, CountIn(pw, kLower + kUpper + kDigits + symbols));
  }
}

TEST(PWPolicyTest, bare_default_uses_preferences)
{
  const PWPolicy def = PWSprefs::GetInstance()->GetDefaultPolicy();
  const PWPolicy bare;
  ASSERT_EQ(0, bare.flags);
  for (int i = 0; i < kRuns; i++) {
    const StringX pw = bare.MakeRandomPassword();
    EXPECT_EQ(static_cast<size_t>(def.length), pw.length());
  }
}

TEST(PWPolicyTest, pronounceable)
{
  PWPolicy pol;
  pol.flags = PWPolicy::UseLowercase | PWPolicy::MakePronounceable;
  pol.length = 12;
  for (int i = 0; i < kRuns; i++) {
    const StringX pw = pol.MakeRandomPassword();
    ASSERT_EQ(12u, pw.length());
    EXPECT_EQ(12, CountIn(pw, kLower));
  }
}

TEST(PWPolicyTest, easy_vision)
{
  PWPolicy pol;
  pol.flags = PWPolicy::UseLowercase | PWPolicy::UseUppercase |
              PWPolicy::UseDigits | PWPolicy::UseEasyVision;
  pol.length = 30;
  pol.lowerminlength = pol.upperminlength = pol.digitminlength = 1;
  for (int i = 0; i < kRuns; i++) {
    const StringX pw = pol.MakeRandomPassword();
    ASSERT_EQ(30u, pw.length());
    EXPECT_EQ(0, CountIn(pw, _T("lIOSZ0125")));
    EXPECT_GE(CountIn(pw, kLower), 1);
    EXPECT_GE(CountIn(pw, kUpper), 1);
    EXPECT_GE(CountIn(pw, kDigits), 1);
  }
}

TEST(PWPolicyTest, hex_only)
{
  PWPolicy pol;
  pol.flags = PWPolicy::UseHexDigits;
  pol.length = 16;
  for (int i = 0; i < kRuns; i++) {
    const StringX pw = pol.MakeRandomPassword();
    ASSERT_EQ(16u, pw.length());
    EXPECT_EQ(16, CountIn(pw, _T("0123456789abcdef")));
  }
}

TEST(PWPolicyTest, custom_symbol_set)
{
  PWPolicy pol;
  pol.flags = PWPolicy::UseLowercase | PWPolicy::UseSymbols;
  pol.length = 10;
  pol.lowerminlength = 1;
  pol.symbolminlength = 3;
  pol.symbols = _T("#@");
  for (int i = 0; i < kRuns; i++) {
    const StringX pw = pol.MakeRandomPassword();
    ASSERT_EQ(10u, pw.length());
    const int nsym = CountIn(pw, _T("#@"));
    EXPECT_GE(nsym, 3);
    EXPECT_EQ(10, nsym + CountIn(pw, kLower));
  }
}

TEST(PWPolicyTest, reserved_bit_with_classes_round_trips)
{
  PWPolicy pol;
  pol.flags = PWPolicy::UseLowercase | PWPolicy::UseDigits | 0x0001;
  pol.length = 12;
  pol.lowerminlength = 2;
  pol.digitminlength = 3;
  const StringX str(pol);
  EXPECT_EQ(StringX(_T("a00100c003002000000")), str);
  const PWPolicy back(str);
  EXPECT_EQ(pol.flags, back.flags);
  EXPECT_EQ(12, back.length);
  EXPECT_EQ(2, back.lowerminlength);
  EXPECT_EQ(3, back.digitminlength);
  EXPECT_EQ(pol, back);
}

TEST(PWPolicyTest, reserved_bit_with_hex_parses_to_empty)
{
  // Flags 0x0801: hex digits plus reserved bit 0x0001, length 16
  const PWPolicy back(StringX(_T("0801010000000000000")));
  EXPECT_EQ(0, back.flags);
  EXPECT_EQ(0, back.length);
  EXPECT_EQ(PWPolicy(), back);
}

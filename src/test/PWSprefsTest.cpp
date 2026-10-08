/*
* Copyright (c) 2026 Robert John Barbour.
* All rights reserved. Use of the code is allowed under the
* Artistic License 2.0 terms, as specified in the LICENSE file
* distributed with this code, or available from
* http://www.opensource.org/licenses/artistic-license-2.0.php
*/
// PWSprefsTest.cpp: Characterisation of passphrase-related application prefs

#ifdef WIN32
#include "../ui/Windows/stdafx.h"
#endif
#include "core/PWSprefs.h"
#include "core/Passphrase.h"
#include "gtest/gtest.h"

TEST(PWSprefsTest, passphrase_prefs_defaults_and_limits)
{
  const PWSprefs *prefs = PWSprefs::GetInstance();

  EXPECT_FALSE(prefs->GetPrefDefVal(PWSprefs::UseLocalPassphrasePolicy));
  EXPECT_FALSE(prefs->GetPref(PWSprefs::UseLocalPassphrasePolicy));

  EXPECT_EQ(static_cast<unsigned int>(kDefaultPassphraseWords),
            prefs->GetPrefDefVal(PWSprefs::PassphraseWordCount));
  EXPECT_EQ(static_cast<unsigned int>(kDefaultPassphraseWords),
            prefs->GetPref(PWSprefs::PassphraseWordCount));
  EXPECT_EQ(1, prefs->GetPrefMinVal(PWSprefs::PassphraseWordCount));
  EXPECT_EQ(99, prefs->GetPrefMaxVal(PWSprefs::PassphraseWordCount));
}

TEST(PWSprefsTest, passphrase_prefs_are_not_stored_in_the_safe)
{
  // Only database-scoped prefs go into the string saved in a safe's header,
  // so changing an application-scoped pref must leave that string unchanged.
  PWSprefs *prefs = PWSprefs::GetInstance();
  prefs->SetupCopyPrefs();
  const StringX before = prefs->Store(true);

  prefs->SetPref(PWSprefs::UseLocalPassphrasePolicy, true, true);
  prefs->SetPref(PWSprefs::PassphraseWordCount, 9u, true);
  EXPECT_TRUE(prefs->GetPref(PWSprefs::UseLocalPassphrasePolicy, true));
  EXPECT_EQ(9u, prefs->GetPref(PWSprefs::PassphraseWordCount, true));
  EXPECT_EQ(before, prefs->Store(true));

  prefs->SetupCopyPrefs();
  EXPECT_FALSE(prefs->GetPref(PWSprefs::UseLocalPassphrasePolicy, true));
}

TEST(PWSprefsTest, existing_enum_positions_unchanged)
{
  // Indices must match upstream 3996b15; the new prefs are last so that
  // database prefs written by index stay compatible with older files.
  EXPECT_EQ(4, static_cast<int>(PWSprefs::UseDefaultUser));
  EXPECT_EQ(68, static_cast<int>(PWSprefs::VKShowTooltips));
  EXPECT_EQ(69, static_cast<int>(PWSprefs::UseLocalPassphrasePolicy));
  EXPECT_EQ(70, static_cast<int>(PWSprefs::NumBoolPrefs));

  EXPECT_EQ(0, static_cast<int>(PWSprefs::Column1Width));
  EXPECT_EQ(36, static_cast<int>(PWSprefs::DisplayMode));
  EXPECT_EQ(37, static_cast<int>(PWSprefs::PassphraseWordCount));
  EXPECT_EQ(38, static_cast<int>(PWSprefs::NumIntPrefs));
}

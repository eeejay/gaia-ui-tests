# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from marionette.marionette import Actions
import json

class TestLockScreenA11y(GaiaTestCase):

    # Windows container in hidden state
    _windows_locator = ('id', 'windows')

    # Lockscreen with buttons permanently showing
    _lockscreen_triggered_locator = ('css selector', '#lockscreen.triggered:not(.elastic)')

    # Lockscreen unlock button
    _unlock_button_locator = ('id', 'lockscreen-area-unlock')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.marionette.execute_script(
            'SpecialPowers.setIntPref("accessibility.accessfu.activate", 0);')

        # this time we need it locked!
        self.lockscreen.lock()

        self.data_layer.set_setting('accessibility.screenreader', True)

    def cleanUp(self):
        GaiaTestCase.cleanUp(self)

        self.marionette.execute_script(
            'SpecialPowers.clearUserPref("accessibility.accessfu.activate");')

        self.data_layer.set_setting('accessibility.screenreader', False)

    def test_lockscreen_a11y(self):
        windows = self.marionette.find_element(*self._windows_locator)

        # Lockscreen should be permanently in 'triggered' state
        self.assertTrue(self.is_element_displayed(*self._lockscreen_triggered_locator))

        # windows container should be hidden with aria-hidden
        self.wait_for_condition(lambda x: self.a11y.is_hidden(windows))

        # tap button to unlock
        unlock_button = self.marionette.find_element(*self._unlock_button_locator)
        unlock_button.click()

        # windows should show after unlock
        self.wait_for_condition(lambda x: not self.a11y.is_hidden(windows))

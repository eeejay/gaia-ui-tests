# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser
from gaiatest.apps.cost_control.app import CostControl


class TestCostControlDataAlertMobile(GaiaTestCase):

    # notification bar locators
    _cost_control_widget_locator = ('css selector', 'iframe[data-frame-origin="app://costcontrol.gaiamobile.org"]')
    _data_usage_view_locator = ('id', 'datausage-limit-view')

    def test_cost_control_data_alert_mobile(self):

        self.data_layer.connect_to_cell_data()
        cost_control = CostControl(self.marionette)
        cost_control.launch()
        cost_control.run_ftu_accepting_defaults()

        self.assertTrue(cost_control.is_mobile_data_tracking_on)
        self.assertFalse(cost_control.is_wifi_data_tracking_on)

        settings = cost_control.tap_settings()
        settings.toggle_data_alert_switch(True)
        settings.select_when_use_is_above_unit_and_value('MB', '0.1')
        settings.reset_data_usage()
        settings.tap_done()

        self.assertEqual(cost_control.mobile_data_usage_figure, '0.00 B')

        # open browser to get some data downloaded
        # please remove this once there is a better way than launching browser app/obj to do so
        browser = Browser(self.marionette)
        browser.launch()
        browser.go_to_url('http://developer.mozilla.org/')

        # get the notification bar
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")

        # switch to cost control widget
        usage_iframe = self.marionette.find_element(*self._cost_control_widget_locator)
        self.marionette.switch_to_frame(usage_iframe)

        # make sure the color changed
        bar = self.marionette.find_element(*self._data_usage_view_locator)
        self.wait_for_condition(lambda m: 'reached-limit' in bar.get_attribute('class'),
                                message='Data usage bar did not breach limit')

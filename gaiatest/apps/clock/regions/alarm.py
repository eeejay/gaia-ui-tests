# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.clock.app import Clock
from marionette.marionette import Actions


class NewAlarm(Clock):

    _picker_container_locator = ('id', 'picker-container')
    _alarm_name_locator = ('xpath', "//input[@placeholder='Alarm']")
    _repeat_menu_locator = ('id', 'repeat-menu')
    _sound_menu_locator = ('id', 'sound-menu')
    _snooze_menu_locator = ('id', 'snooze-menu')
    _done_locator = ('id', 'alarm-done')

    _hour_picker_locator = ('css selector', '#value-picker-hours div')
    _minutes_picker_locator = ('css selector', '#value-picker-minutes div')
    _hour24_picker_locator = ('css selector', '#value-picker-hour24-state div')

    @property
    def alarm_label(self):
        return self.marionette.find_element(*self._alarm_name_locator).text

    def type_alarm_label(self, value):
        label = self.marionette.find_element(*self._alarm_name_locator)
        label.clear()
        label.send_keys(value)

    @property
    def alarm_label_placeholder(self):
        return self.marionette.find_element(*self._alarm_name_locator).get_attribute('placeholder')

    @property
    def alarm_repeat(self):
        return self.marionette.find_element(*self._repeat_menu_locator).text

    def select_repeat(self, value):
        self.marionette.tap(self.marionette.find_element(*self._repeat_menu_locator))
        self.select(value)

    @property
    def alarm_snooze(self):
        return self.marionette.find_element(*self._snooze_menu_locator).text

    def select_snooze(self, value):
        self.marionette.tap(self.marionette.find_element(*self._snooze_menu_locator))
        self.select(value)

    @property
    def alarm_sound(self):
        return self.marionette.find_element(*self._sound_menu_locator).text

    def select_sound(self, value):
        self.marionette.tap(self.marionette.find_element(*self._sound_menu_locator))
        self.select(value)

    def wait_for_picker_to_be_visible(self):
        self.wait_for_element_displayed(*self._picker_container_locator)

    def tap_done(self):
        self.marionette.tap(self.marionette.find_element(*self._done_locator))

        clock = Clock(self.marionette)
        clock.wait_for_banner_displayed()
        return clock

    @property
    def current_hour(self):
        return self.marionette.find_element(*self._current_element(*self._hour_picker_locator)).text

    def spin_hour(self):
        current_hour = int(self.current_hour)
        if current_hour > 6:
                self._flick_menu_down(self._hour_picker_locator)
        else:
            self._flick_menu_up(self._hour_picker_locator)
        time.sleep(1)

    @property
    def current_minute(self):
        return self.marionette.find_element(*self._current_element(*self._minutes_picker_locator)).text

    def spin_minute(self):
        current_minute = int(self.current_minute)
        if current_minute > 30:
            self._flick_menu_down(self._minutes_picker_locator)
        else:
            self._flick_menu_up(self._minutes_picker_locator)

        time.sleep(1)

    @property
    def current_hour24(self):
        return self.marionette.find_element(*self._current_element(*self._hour24_picker_locator)).text

    def spin_hour24(self):
        current_hour = self.current_hour24
        if current_hour == 'AM':
            self.marionette.flick(self.marionette.find_element(*self._current_element(*self._hour24_picker_locator)),
                                  '50%', '50%',
                                  0, -300,
                                  800)
        else:
            self.marionette.flick(self.marionette.find_element(*self._current_element(*self._hour24_picker_locator)),
                                  '50%', '50%',
                                  0, 300,
                                  800)

        time.sleep(1)

    def _flick_menu_up(self, locator):
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        action = Actions(self.marionette)
        action.press(next_element)
        action.move(current_element)
        action.release()
        action.perform()

    def _flick_menu_down(self, locator):
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        action = Actions(self.marionette)
        action.press(current_element)
        action.move(next_element)
        action.release()
        action.perform()

    def _current_element(self, method, target):
        return (method, '%s.picker-unit.active' % target)

    def _next_element(self, method, target):
        return (method, '%s.picker-unit.active + div' % target)


class EditAlarm(NewAlarm):

    _alarm_delete_button_locator = ('id', 'alarm-delete')

    def __init__(self, marionette):
        NewAlarm.__init__(self, marionette)
        self.wait_for_element_displayed(*self._alarm_delete_button_locator)

    def tap_delete(self):
        self.marionette.tap(self.marionette.find_element(*self._alarm_delete_button_locator))
        return Clock(self.marionette)

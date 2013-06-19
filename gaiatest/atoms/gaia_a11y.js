/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

'use strict';

var GaiaA11y = {

  isHidden: function GaiaA11y_isHidden(element) {
    let style = window.wrappedJSObject.getComputedStyle(element.wrappedJSObject);
    if (style.visibility == 'hidden' || style.display == 'none') {
      return true;
    }

    let elem = element.wrappedJSObject;
    do {
      if (JSON.parse(elem.getAttribute('aria-hidden'))) {
        return true;
      }

      elem = elem.parentNode;
    } while (elem && elem.getAttribute);

    return false;
  }
};

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.gallery.app import Gallery


class TestGalleryEditPhoto(GaiaTestCase):

    _edit_effect_button_locator = ('id', 'edit-effect-button')
    _effect_options_locator = ('css selector', '#edit-effect-options a')
    _edit_save_locator = ('id', 'edit-save-button')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_edit_photo(self):
        gallery = Gallery(self.marionette)
        gallery.launch()
        gallery.wait_for_files_to_load(1)

        self.assertTrue(gallery.gallery_items_number > 0)

        image = gallery.tap_first_gallery_item()

        # Tap on Edit button.
        edit_image = image.tap_edit_button()

        # Tap on Effects button.
        edit_image.tap_edit_effects_button()

        # Change effects.
        [effect.tap() for effect in edit_image.effects]

        # TBD. Verify the photo is changed.

        gallery = edit_image.tap_edit_save_button()
        gallery.wait_for_files_to_load(2)

        # Verify new Photo is created
        self.assertEqual(2, gallery.gallery_items_number)

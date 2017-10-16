# Copyright 2017, DigitalGlobe, Inc.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.

import glob2
import json
import os

import beachfront.vectorize as bfvec
import gippy

from gbdx_task_interface import GbdxTaskInterface

# defaults
defaults = {
    'minsize': 100.0,
    'close': 5,
    'smooth': 0.0,
}


class PotraceTask(GbdxTaskInterface):
    gbdx_connection = None

    def invoke(self):

        # Get inputs
        img = self.get_input_data_port('image')
        threshold = self.get_input_string_port('threshold')

        result_dir = self.get_output_data_port('result')
        os.makedirs(result_dir)

        # vectorize threshdolded (ie now binary) image
        all_lower = glob2.glob('%s/**/*.tif' % img)

        for img_file in all_lower:
            geoimg = gippy.GeoImage(img_file, True)
            coastline = bfvec.potrace(
                geoimg[0] > threshold, minsize=defaults['minsize'], close=defaults['close'], alphamax=defaults['smooth'])

            # convert coordinates to GeoJSON
            geojson = bfvec.to_geojson(coastline, source=geoimg.basename())

            # write geojson output file
            with open(os.path.join(result_dir, 'result.geojson'), 'w') as f:
                f.write(json.dumps(geojson))

        self.reason = 'Successfully traced raster'


if __name__ == "__main__":
    with PotraceTask() as task:
        task.invoke()

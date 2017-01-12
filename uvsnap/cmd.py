#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""UVSnap Commands."""

import argparse
import os
import tempfile
import time

import uvsnap

__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def get_all_snapshots():
    """Command Line interface for UVSnap."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-n', '--nvr_url', help='NVR URL'
    )
    parser.add_argument(
        '-a', '--api_key', help='API_KEY'
    )
    parser.add_argument(
        '-d', '--directory', help='Snapshot Directory', default=tempfile.mkdtemp()
    )

    opts = parser.parse_args()

    if not os.path.exists(opts.directory):
        os.makedirs(opts.directory)

    nvr = uvsnap.NVR(opts.nvr_url, opts.api_key)
    snapshots = nvr.get_all_snapshots()

    for camera_id, snapshot in snapshots.iteritems():
        if snapshot is not None:
            output_file = os.path.join(opts.directory, '%s.jpg' % camera_id)

            with open(output_file, 'w') as ofd:
                ofd.write(snapshot)
            print 'wrote %s' % output_file

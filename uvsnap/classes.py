
import json
import requests


requests.packages.urllib3.disable_warnings()


class NVR(object):

    def __init__(self, nvr_url, api_key):
        self.nvr_url = nvr_url
        self.api_key = api_key

        self.cameras = []

    def get_cameras(self):
        cameras_url = "%s/api/2.0/camera" % self.nvr_url

        get_cameras = requests.get(
            cameras_url,
            params={'apiKey': self.api_key},
            verify=False
        )

        if get_cameras.ok:
            cameras = json.loads(get_cameras.text)
            self.cameras = cameras['data']

    def _get_snapshot(self, camera_id):
        if not self.cameras:
            self.get_cameras()

        for camera in self.cameras:
            if camera['state'] == 'CONNECTED' and camera['_id'] == camera_id:
                get_snapshot = requests.get(
                    "%s/api/2.0/snapshot/camera/%s" % (self.nvr_url, camera_id),
                    params={'force': 'true', 'apiKey': self.api_key},
                    verify=False
                )

                if get_snapshot.ok:
                    return get_snapshot

    def get_snapshot(self, camera_id):
        snapshot = self._get_snapshot(camera_id)
        if snapshot:
            return snapshot.content

    def get_snapshot_url(self, camera_id):
        snapshot = self._get_snapshot(camera_id)
        if snapshot:
            return snapshot.url

    def get_all_snapshots(self):
        snapshots = {}

        if not self.cameras:
            self.get_cameras()

        for camera in self.cameras:
            snapshots[camera['_id']] = self.get_snapshot(camera['_id'])
        return snapshots

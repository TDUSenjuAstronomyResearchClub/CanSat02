import unittest

import cansatapi.message.jsonGenerator


class TestJsonGenerator(unittest.TestCase):

    def test_generate_msg_json(self):
        date = "9999/09/09-0:20:10"
        msg = "test"
        json_data = cansatapi.message.jsonGenerator.generate_json(time=date, message=msg)
        self.assertEqual(json_data, '{"time": "9999/09/09-0:20:10", "gps": null, "nine_axis": null, "bme280": null, '
                                    '"lps25hb": null, "battery": null, "distance": null, "camera": null, '
                                    '"soil_moisture": null, "message": "test"}')
